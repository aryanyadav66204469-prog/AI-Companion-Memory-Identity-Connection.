from deepface import DeepFace

def find_person(uploaded_image_path, memories):

    best_match = None
    best_distance = float("inf")

    for person in memories:
        try:
            result = DeepFace.verify(
                img1_path=uploaded_image_path,
                img2_path=person["image"],
                enforce_detection=False
            )

            if result["verified"]:
                if result["distance"] < best_distance:
                    best_distance = result["distance"]
                    best_match = person

        except:
            continue

    return best_match