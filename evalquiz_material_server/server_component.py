import mimetypes
import os
import asyncio
from blake3 import blake3
from pathlib import Path
from evalquiz_proto.shared.exceptions import (
    FirstDataChunkNotMetadataException,
    NoMimetypeMappingException,
)
from evalquiz_proto.shared.generated import (
    MaterialServerBase,
    Empty,
    ListOfStrings,
    MaterialUploadData,
    Metadata,
    String,
)
from grpclib.server import Server
from typing import AsyncIterator
from evalquiz_proto.shared.path_dictionary_controller import (
    PathDictionaryController,
)
import betterproto


class MaterialServerService(MaterialServerBase):
    """Serves endpoints for material manipulation."""

    def __init__(
        self,
        material_storage_path: Path,
        path_dictionary_controller: PathDictionaryController = PathDictionaryController(),
    ) -> None:
        """Constructor of MaterialServerService.

        Args:
            material_storage_path (Path): Specifies the path where lecture materials are stored.
            path_dictionary_controller: (PathDictionaryController): A custom material controller can be passed as an argument, otherwise a PathDictionaryController with default arguments is initialized.
        """
        self.material_storage_path = material_storage_path
        self.path_dictionary_controller = path_dictionary_controller

    async def upload_material(
        self, material_upload_data_iterator: AsyncIterator["MaterialUploadData"]
    ) -> "Empty":
        """Asynchronous method that is used by gRPC as an endpoint.
        Manages a lecture material upload.
        Note on how local_path is built: The file extension is added to the hash to enable mimetype recognition when loading the lecture material:
        When PathDictionaryController.load_file is invoked.

        Args:
            material_upload_data_iterator (AsyncIterator[MaterialUploadData]): An Iterator which elements represent packages of the stream. Includes a Metadata instance as the first element and data in bytes as the following elements.

        Raises:
            FirstDataChunkNotMetadataException: Raised, if the first element is not a Metadata instance.
            NoMimetypeMappingException: The mimetype in lecture_material.file_type could not be mapped to a file extension.

        Returns:
            Empty: Empty gRPC compatible return format. Equivalent to "None".
        """
        material_upload_data = await material_upload_data_iterator.__anext__()
        (type, metadata) = betterproto.which_one_of(
            material_upload_data, "material_upload_data"
        )
        if metadata is not None and type == "metadata":
            extension = mimetypes.guess_extension(metadata.mimetype)
            if extension is None:
                raise NoMimetypeMappingException()
            async_iterator_bytes = self._to_async_iterator_bytes(
                material_upload_data_iterator
            )
            load_local_path = await self._load_from_binary_iterator(
                async_iterator_bytes
            )
            hash = self._calculate_hash(load_local_path)
            local_path = self.material_storage_path / hash
            local_path = local_path.parent / (local_path.name + extension)
            self.path_dictionary_controller.copy_and_load_file(
                load_local_path, local_path, hash, metadata.name
            )
            return Empty()
        raise FirstDataChunkNotMetadataException()

    async def _load_from_binary_iterator(
        self, binary_iterator: AsyncIterator[bytes]
    ) -> Path:
        """Loads file from binary into into `/tmp` folder.

        Args:
            binary_iterator (AsyncIterator[bytes]): Binary iterator to work with.

        Returns:
            Path: Path to the file in `/tmp`.
        """
        local_path = Path("/tmp/current_evalquiz_upload")
        with open(local_path, "ab") as local_file:
            local_file.truncate(0)
            while True:
                try:
                    data = await binary_iterator.__anext__()
                    local_file.write(data)
                except StopAsyncIteration:
                    break
        return local_path

    def _calculate_hash(self, local_path: Path) -> str:
        """Calculates blake3 hash of local file.

        Args:
            local_path (Path): Path to local file.

        Returns:
            str: Resulting hash.
        """
        with open(local_path, "rb") as local_file:
            file_content = local_file.read()
            return blake3(file_content).hexdigest()

    async def _to_async_iterator_bytes(
        self, material_upload_data_iterator: AsyncIterator[MaterialUploadData]
    ) -> AsyncIterator[bytes]:
        """Converts AsyncIterator[MaterialUploadData] to AsyncIterator[bytes] by runtime type checking/assertions.

        Args:
            material_upload_data_iterator (AsyncIterator[MaterialUploadData]): Iterator of MaterialUploadData.

        Returns:
            AsyncIterator[bytes]: Iterator of bytes.
        """
        material_upload_data = await material_upload_data_iterator.__anext__()
        (type, data) = betterproto.which_one_of(
            material_upload_data, "material_upload_data"
        )
        if data is not None and type == "data":
            yield data
        else:
            TypeError(
                "AsyncIterator[MaterialUploadData] cannot be converted into AsyncIterator[bytes]."
            )

    async def delete_material(self, string: "String") -> "Empty":
        """Asynchronous method that is used by gRPC as an endpoint.
        Manages deletion of lecture materials

        Args:
            string (String): The hash of the lecture material.

        Returns:
            Empty: Empty gRPC compatible return format. Equivalent to "None".
        """
        self.path_dictionary_controller.delete_file(string.value)
        return Empty()

    async def get_material_hashes(self, empty: "Empty") -> "ListOfStrings":
        """Asynchronous method that is used by gRPC as an endpoint.
        Returns hashes of all registered lecture materials.

        Args:
            empty (Empty): Empty gRPC compatible return format. Equivalent to "None". Required as parameter.

        Returns:
            ListOfStrings: Hashes of all registered lecture materials.
        """
        material_hashes = self.path_dictionary_controller.get_material_hashes()
        return ListOfStrings(material_hashes)

    async def get_material_name(self, string: "String") -> "String":
        """Asynchronous method that is used by gRPC as an endpoint.
        Returns material name of a lecture material hash.

        Args:
            string (String): The hash of the lecture material.

        Returns:
            String: Material name, as specified in PathDictionaryController.
        """
        hash = string.value
        name = self.path_dictionary_controller.get_material_name(hash)
        return String(name)

    async def get_material(
        self, string: "String"
    ) -> "AsyncIterator[MaterialUploadData]":
        """Asynchronous method that is used by gRPC as an endpoint.
        Returns a specific lecture material for a hash.

        Args:
            string (String): Hash of the material to query.

        Returns:
            AsyncIterator[MaterialUploadData]: An Iterator which elements represent packages of the stream. Includes LectureMaterial as the first element and data in bytes as the following elements.
        """
        (
            mimetype,
            material_upload_iterator,
        ) = await self.path_dictionary_controller.get_file_from_hash_async(string.value)
        metadata = Metadata(mimetype, string.value)
        yield MaterialUploadData(metadata=metadata)
        while True:
            try:
                data = await material_upload_iterator.__anext__()
                material_upload_data = MaterialUploadData(data=data)
                yield material_upload_data
            except StopAsyncIteration:
                break


async def main() -> None:
    """Sets up and starts MaterialServerService."""
    material_storage_path = Path(__file__).parent / "lecture_materials"
    if not os.path.exists(material_storage_path):
        os.makedirs(material_storage_path)
    server = Server([MaterialServerService(material_storage_path)])
    await server.start("127.0.0.1", 50051)
    print("Server started at port 50051.", flush=True)
    await server.wait_closed()


if __name__ == "__main__":
    """Prevents accidental execution of the server via import."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
