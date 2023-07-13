class MimetypeMismatchException(Exception):
    """Expected mimetype does not match the given mimetype."""

    pass

class MaterialAlreadyLoaded(Exception):
    """InternalLectureMaterial is already available."""