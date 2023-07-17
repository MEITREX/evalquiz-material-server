import glob
import os
from typing import Any, AsyncGenerator, Generator, Iterable
from grpclib.testing import ChannelFor
from pathlib import Path
import pytest
from evalquiz_material_server.server_component import MaterialServerService
from evalquiz_proto.shared.generated import (
    Empty,
    MaterialServerStub,
    LectureMaterial,
    MaterialUploadData,
)

pytest_plugins = ("pytest_asyncio",)


async def to_async_iter(input: Iterable[Any]) -> AsyncGenerator[Any, None]:
    """Helper function to create asynchronous iterator of an Iteratble object, for example a list.

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
        An list with MaterialUploadData elements,
        containing a LectureMaterial at the first index
        and binary data of an example file.
    """
    lecture_material = LectureMaterial(
        "Example material",
        None,
        "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262",
        "text/plain",
        None,
    )
    path = (
        Path(__file__).parent
        / "../../evalquiz_proto/tests/shared/example_materials/example.txt"
    )
    with open(path, "rb") as local_file:
        file_content = local_file.read()
    lecture_material_material_upload_data = MaterialUploadData(
        lecture_material=lecture_material
    )
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
    material_storage_path = Path(__file__).parent / "lecture_materials"
    if not os.path.exists(material_storage_path):
        os.makedirs(material_storage_path)
    material_server_service = MaterialServerService(material_storage_path)
    yield material_server_service
    file_upload_cleanup(material_storage_path)


def test_start_service(material_server_service: MaterialServerService) -> None:
    pass


@pytest.mark.asyncio
async def test_server_upload_material(
    material_server_service: MaterialServerService,
) -> None:
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
    async with ChannelFor([material_server_service]) as channel:
        service = MaterialServerStub(channel)
        material_upload_data = prepare_material_upload_data()
        response = await service.upload_material(material_upload_data)
        assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_client_upload_material_multiple_binaries(
    material_server_service: MaterialServerService,
) -> None:
    async with ChannelFor([material_server_service]) as channel:
        service = MaterialServerStub(channel)
        material_upload_data = prepare_material_upload_data()
        material_upload_data.append(material_upload_data[1])
        response = await service.upload_material(material_upload_data)
        assert isinstance(response, Empty)
