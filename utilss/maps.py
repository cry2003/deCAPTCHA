import os


def create_class_label_mapping(root_dir):
    class_to_label = {}

    labels_dir = os.path.join(root_dir, "labels")
    images_dir = os.path.join(root_dir, "images")

    if (
        not os.path.exists(images_dir)
        or not os.path.isdir(images_dir)
        and not len(os.listdir(images_dir)) == 0
    ):
        raise ValueError(
            f"La directory 'images' non esiste o non è una directory valida in {root_dir}"
        )

    if (
        not os.path.exists(labels_dir)
        or not os.path.isdir(labels_dir)
        and not len(os.listdir(labels_dir)) == 0
    ):
        raise ValueError(
            f"La directory 'images' non esiste o non è una directory valida in {root_dir}"
        )
    img_list = []
    label_list = []
    for class_name in os.listdir(images_dir):
        for label_name in os.listdir(labels_dir):
            if class_name == label_name:
                for img in os.listdir(os.path.join(images_dir, class_name)):
                    img_list.append(img)
                for label in os.listdir(os.path.join(labels_dir, label_name)):
                    label_list.append(label)

    img_list.sort()
    label_list.sort()

    for img in img_list:
        for label in label_list:
            if (
                os.path.splitext(os.path.basename(img))[0]
                == os.path.splitext(os.path.basename(label))[0]
            ):
                class_to_label[img] = label

    return class_to_label
