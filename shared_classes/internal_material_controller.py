from generated import PageFilter, LectureMaterial
from typing import ByteString, Optional
from shared_classes.internal_lecture_material import InternalLectureMaterial


class InternalMaterialController:
    """The InternalMaterialController manages accesses to the local file system,
    containing relevant lecture materials.
    """

    internal_lecture_materials: dict[InternalLectureMaterial]

    def get_material_from_hash(self, hash: str) -> InternalLectureMaterial:
        """A material that exists as an internal representation can be retrieved using a hash.

        Args:
            hash: A blake3 hash generated using the material.
        """
        return self.internal_lecture_materials[hash]

    def load_material(self, local_path: str, lecture_material: LectureMaterial) -> None:
        """Adds a material to the internal pool of lecture materials.

        Args:
            local_path: The system path to the file.
            lecture_material: Information about the lecture material.
        """
        internal_lecture_material = InternalLectureMaterial(
            local_path, lecture_material
        )
        if internal_lecture_material.hash not in self.internal_lecture_materials:
            self.internal_lecture_materials[internal_lecture_material.hash]

    def unload_material(self, hash: str) -> None:
        """Removes the internal representation of a lecture material. Does not delete the file.

        Args:
            hash: A blake3 hash generated using the material.
        """
        self.internal_lecture_materials[hash]

    def add_material(
        self,
        local_path: str,
        lecture_material: LectureMaterial,
        binary: ByteString,
        overwrite: bool = True,
    ) -> InternalLectureMaterial:
        """A new material is created at the specified location.

        Args:
            local_path: The system path to the location where the file is created.
            lecture_material: Information about the lecture material.
            binary: The file itself.
            overwrite: Boolean to describe if an existing file can be overwritten.
        """
        with open(local_path, "r") as local_file:
            file_content = local_file.read()
            hash = blake3(file_content)
        if hash not in self.internal_lecture_materials:
            with open(local_path, 'w') as local_file:
                local_file.write(binary)
            internal_lecture_material = InternalLectureMaterial(
                local_path, lecture_material
            )



    def delete_material(self, local_path: str) -> None:
        """Deletes the internal representation of the file in memory and the file itself from the filesystem.

        Args:
            local_path: The system path to the file.
        """

    def get_material_hashes(self) -> list[str]:
        """Retrieves all hashes of the internally referenced materials.

        Returns:
            A set of strings
        """
        return self.internal_lecture_materials.keys()