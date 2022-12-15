from bpy.types import PropertyGroup, bpy_prop_collection


def list_add(items: bpy_prop_collection) -> int:
    items.add()
    return len(items) - 1


def list_remove(items: bpy_prop_collection, index: int) -> int:
    items.remove(index)
    return max(0, index - 1)


def list_copy(items: bpy_prop_collection, index: int) -> int:
    items.add()

    old: PropertyGroup = items[index]
    new: PropertyGroup = items[-1]

    for key, value in old.items():
        new[key] = value

    return len(items) - 1


def list_move(items: bpy_prop_collection, index: int, direction: int) -> int:
    neighbor = max(0, index + direction)
    length = max(0, len(items) - 1)

    items.move(neighbor, index)
    return max(0, min(neighbor, length))
