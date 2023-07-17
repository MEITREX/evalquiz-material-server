import asyncio
import mimetypes
import os
from pathlib import Path
from evalquiz_proto.shared.exceptions import (
    FirstDataChunkNotLectureMaterialException,
    NoMimetypeMappingException,
)
from evalquiz_proto.shared.generated import (
    MaterialServerBase,
    Empty,
    ListOfStrings,
    MaterialUploadData,
    String,
    LectureMaterial,
)
from grpclib.server import Server
from typing import AsyncIterator
from evalquiz_proto.shared.internal_material_controller import (
    InternalMaterialController,
)
import betterproto


class MaterialServerService(MaterialServerBase):
    """Serves endpoints for material manipulation."""

    def __init__(self, material_storage_path: Path) -> None:
        self.internal_material_controller = InternalMaterialController()
        self.material_storage_path = material_storage_path

    async def upload_material(
        self, material_upload_data_iterator: AsyncIterator["MaterialUploadData"]
    ) -> "Empty":
        """Asynchronous method that is used by gRPC as an endpoint.
        Manages a lecture material upload.

        Args:
            material_upload_data_iterator (AsyncIterator[MaterialUploadData]): Included LectureMaterial as the first element and data in bytes as the following elements.

        Raises:
            FirstDataChunkNotLectureMaterialException: Raised, if the first element is not a LectureMaterial.
            NoMimetypeMappingException: The mimetype in lecture_material.file_type could not be mapped to a file extension.

        Returns:
            Empty: Empty gRPC compatible return format. Equivalent to "None".
        """
        material_upload_data = await material_upload_data_iterator.__anext__()
        (type, lecture_material) = betterproto.which_one_of(
            material_upload_data, "material_upload_data"
        )
        if lecture_material is not None and type == "lecture_material":
            extension = mimetypes.guess_extension(lecture_material.file_type)
            if extension is None:
                raise NoMimetypeMappingException()
            local_path = self.material_storage_path / lecture_material.hash
            local_path = local_path.parent / (local_path.name + extension)
            await self.internal_material_controller.add_material_async(
                local_path,
                lecture_material,
                material_upload_data_iterator,
            )
            return Empty()
        raise FirstDataChunkNotLectureMaterialException()

    async def delete_material(self, string: "String") -> "Empty":
        """Asynchronous method that is used by gRPC as an endpoint.
        Manages deletion of lecture materials

        Args:
            string (String): The hash of the lecture material.

        Returns:
            Empty: Empty gRPC compatible return format. Equivalent to "None".
        """
        self.internal_material_controller.delete_material(string.value)
        return Empty()

    async def get_material_hashes(self, empty: "Empty") -> "ListOfStrings":
        """Asynchronous method that is used by gRPC as an endpoint.
        Returns hashes of all registered lecture materials.

        Args:
            empty (Empty): Empty gRPC compatible return format. Equivalent to "None". Required as parameter.

        Returns:
            ListOfStrings: Hashes of all registered lecture materials.
        """
        material_hashes = self.internal_material_controller.get_material_hashes()
        return ListOfStrings(material_hashes)

    async def get_material(self, string: "String") -> "LectureMaterial":
        """Asynchronous method that is used by gRPC as an endpoint.
        Returns a specific lecture material for a hash.

        Args:
            string (String): Hash of the material to query.

        Returns:
            LectureMaterial: LectureMaterial referenced by the hash.
        """
        return self.internal_material_controller.get_material_from_hash(string.value)


async def main() -> None:
    """Sets up and starts MaterialServerService."""
    material_storage_path = Path(__file__).parent / "lecture_materials"
    if not os.path.exists(material_storage_path):
        os.makedirs(material_storage_path)
    server = Server([MaterialServerService(material_storage_path)])
    await server.start("127.0.0.1", 50051)
    await server.wait_closed()


if __name__ == "__main__":
    """Prevents accidental execution of the server via import."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
