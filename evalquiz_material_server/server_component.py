import asyncio
from pathlib import Path
from evalquiz_proto.shared.exceptions import (
    DataChunkNotBytesException,
    EmptyUploadException,
    FirstDataChunkNotLectureMaterialException,
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
from typing import AsyncIterator, List, Union
from evalquiz_proto.shared.internal_material_controller import InternalMaterialController
import betterproto


class MaterialServerService(MaterialServerBase):
    """Serves endpoints for material manipulation."""

    def __init__(self, material_storage_path: Path) -> None:
        self.internal_material_controller = InternalMaterialController()
        self.material_storage_path = material_storage_path

    async def upload_material(
        self, material_upload_data_iterator: AsyncIterator["MaterialUploadData"]
    ) -> "Empty":
        material_upload_data = await material_upload_data_iterator.__anext__()
        (
            type,
            lecture_material
        ) = betterproto.which_one_of(material_upload_data, "material_upload_data")
        if lecture_material is not None and type == "lecture_material":
            await self.internal_material_controller.add_material_async(
                self.material_storage_path, lecture_material, material_upload_data_iterator
            )
            return Empty()
        raise FirstDataChunkNotLectureMaterialException()

    async def delete_material(self, string: "String") -> "Empty":
        self.internal_material_controller.delete_material(string.value)
        return Empty()

    async def get_material_hashes(self, empty: "Empty") -> "ListOfStrings":
        material_hashes = self.internal_material_controller.get_material_hashes()
        return ListOfStrings(material_hashes)

    async def get_material(self, string: "String") -> "LectureMaterial":
        return self.internal_material_controller.get_material_from_hash(string.value)


async def main() -> None:
    material_storage_path = Path("./lecture_materials")
    server = Server([MaterialServerService(material_storage_path)])
    await server.start("127.0.0.1", 50051)
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
