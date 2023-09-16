import glob
import os
from typing import Any, AsyncGenerator, Generator, Iterable, List
from blake3 import blake3
from grpclib.testing import ChannelFor
from pathlib import Path
from pymongo import MongoClient
import pytest
from evalquiz_material_server.server_component import MaterialServerService
from evalquiz_proto.shared.generated import (
    Empty,
    MaterialServerStub,
    LectureMaterial,
    MaterialUploadData,
    Metadata,
    String,
)
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.path_dictionary_controller import (
    PathDictionaryController,
)

pytest_plugins = ("pytest_asyncio",)


async def to_async_iter(input: Iterable[Any]) -> AsyncGenerator[Any, None]:
    """Helper function to create asynchronous iterator of an Iterable object, for example a list.

    Args:
        input: The Iterable object

    Returns:
        An asynchronous generator with the contents of the Iterable object.
    """
    for x in input:
        yield x


def prepare_material_upload_data() -> list[MaterialUploadData]:
    """Data preparation function to create example upload data.

    Returns:
        A list with MaterialUploadData elements,
        containing a LectureMaterial at the first index
        and binary data of an example file.
    """
    metadata = Metadata(
        "text/plain",
        "f9f75c3c05c99d69364ae75e028c997fb1a8c209e03a6452efbef6b75784c3ab",
    )
    path = (
        Path(__file__).parent
        / "../../evalquiz_proto/tests/shared/example_materials/example.txt"
    )
    with open(path, "rb") as local_file:
        file_content = local_file.read()
    lecture_material_material_upload_data = MaterialUploadData(metadata=metadata)
    file_content_material_upload_data = MaterialUploadData(data=file_content)
    material_upload_data = [
        lecture_material_material_upload_data,
        file_content_material_upload_data,
    ]
    return material_upload_data


def delete_all_files_in_folder(folder_path: Path) -> None:
    """Deletes all files in a folder, non-recursive.

    Args:
        folder_path (Path): Path to the folder.
    """
    files = glob.glob(str(folder_path / "*"))
    for local_file in files:
        os.remove(local_file)


def file_upload_cleanup(material_storage_path: Path) -> None:
    """Deletes files that were uploaded for test purposes.

    Args:
        material_storage_path (Path): The path were the uploaded files are stored.
    """
    delete_all_files_in_folder(material_storage_path)
    os.rmdir(material_storage_path)


@pytest.fixture(scope="session")
def material_server_service() -> Generator[MaterialServerService, None, None]:
    """Pytest fixture of MaterialServerService.
    Initializes PathDictionaryController with custom test database.
    Test database is emptied before tests are executed.
    Cleans up created files after test execution that uses this fixture.

    Yields:
        Generator[MaterialServerService, None, None]: Generator with one MaterialServerService element. Yielded until file cleanup.
    """
    material_storage_path = Path(__file__).parent / "lecture_materials"
    if not os.path.exists(material_storage_path):
        os.makedirs(material_storage_path)
    path_dictionary_controller = PathDictionaryController(
        mongodb_database="local_path_test_db"
    )
    path_dictionary_controller.mongodb_client.drop_database("lecture_material_test_db")
    material_server_service = MaterialServerService(
        material_storage_path, path_dictionary_controller
    )
    yield material_server_service
    file_upload_cleanup(material_storage_path)


@pytest.mark.asyncio
async def test_server_upload_material(
    material_server_service: MaterialServerService,
) -> None:
    """Tests MaterialServerService upload_material method.

    Args:
        material_server_service (MaterialServerService): Pytest fixture of MaterialServerService
    """
    material_upload_data = prepare_material_upload_data()
    material_upload_data_iterator = to_async_iter(material_upload_data)
    response = await material_server_service.upload_material(
        material_upload_data_iterator
    )
    assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_client_upload_material(
    material_server_service: MaterialServerService,
) -> None:
    """Tests MaterialServerService upload_material method with client-server connection.

    Args:
        material_server_service (MaterialServerService): Pytest fixture of MaterialServerService
    """
    async with ChannelFor([material_server_service]) as channel:
        service = MaterialServerStub(channel)
        material_upload_data = prepare_material_upload_data()
        response = await service.upload_material(material_upload_data)
        assert isinstance(response, Empty)


def calculate_combined_file_hash(material_upload_data: List[MaterialUploadData]) -> str:
    """Calculated the hash for a partitioned upload, as if it was one file.

    Args:
        material_upload_data (List[MaterialUploadData]): List of MaterialUploadData containing LectureMaterial at the first index followed by binary data.

    Returns:
        str: Calculated hash.
    """
    combined_data = b""
    for data in material_upload_data[1:]:
        combined_data += data.data
    return blake3(combined_data).hexdigest()


@pytest.mark.asyncio
async def test_client_upload_material_multiple_binaries(
    material_server_service: MaterialServerService,
) -> None:
    """Tests MaterialServerService upload_material method with a partitioned binary that is sent in multiple gRPC stream packets.
    The partitioned binary is combined to validate the correctness of the received file by the server.
    A combined file hash is calculated to test the correctness of the received file.

    Args:
        material_server_service (MaterialServerService): Pytest fixture of MaterialServerService
    """
    async with ChannelFor([material_server_service]) as channel:
        service = MaterialServerStub(channel)
        material_upload_data = prepare_material_upload_data()
        material_upload_data.append(material_upload_data[1])
        combined_file_hash = calculate_combined_file_hash(material_upload_data)
        assert (
            combined_file_hash
            == "4ae07713320c64171db6d4c5c7316d643c45eefcb0c36c2e566eb2f3b837cdb8"
        )
        material_upload_data[
            0
        ].metadata.name = (
            "4ae07713320c64171db6d4c5c7316d643c45eefcb0c36c2e566eb2f3b837cdb8"
        )
        response = await service.upload_material(material_upload_data)
        assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_server_get_material(
    material_server_service: MaterialServerService,
) -> None:
    """Tests MaterialServerService get_material method with client-server connection.

    Args:
        material_server_service (MaterialServerService): Pytest fixture of MaterialServerService
    """
    material_upload_data = prepare_material_upload_data()
    material_upload_data_iterator = to_async_iter(material_upload_data)
    await material_server_service.upload_material(material_upload_data_iterator)
    async_iterator = material_server_service.get_material(
        String(material_upload_data[0].metadata.name)
    )
    lecture_material_material_upload_data = await async_iterator.__anext__()
    file_content_material_upload_data = await async_iterator.__anext__()
    assert material_upload_data == [
        lecture_material_material_upload_data,
        file_content_material_upload_data,
    ]


def test_pymongo_connection() -> None:
    """Tests if connection to database can be established."""
    client: MongoClient[dict[str, Any]] = MongoClient("db", 27017)
    client.drop_database("lecture_material_test_db")
    lecture_material_test_db = client.lecture_material_test_db
    internal_lecture_materials = lecture_material_test_db.internal_lecture_materials
    internal_lecture_material = InternalLectureMaterial(
        Path(__file__).parent
        / "../../evalquiz_proto/tests/shared/example_materials/modified_example.txt",
        LectureMaterial(
            reference="Modified example textfile",
            hash="068aee4ee49d6cabb1576286108939205260d07cadeaaa249b352487bfe4bc3d",
            file_type="text/plain",
        ),
    )
    mongodb_document = internal_lecture_material.to_mongodb_document()
    internal_lecture_materials.insert_one(mongodb_document)
