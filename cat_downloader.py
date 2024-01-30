import argparse
import os
import requests

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"  # Replace this with your actual cat API URL
SAVE_DIR = "cat_images"


def download_cat_images(num_images, breed=None, color=None):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        params = {'limit': num_images}
        if breed:
            params['breed_ids'] = breed
        if color:
            params['mime_types'] = 'jpg,png'
            params['colors'] = color

        images_downloaded = 0
        page = 1
        while images_downloaded < num_images:
            params['page'] = page
            response = requests.get(CAT_API_URL, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            cat_data = response.json()
            if isinstance(cat_data, list) and len(cat_data) > 0:
                for cat in cat_data:
                    cat_url = cat.get('url')
                    if cat_url:
                        image_name = f"cat_{images_downloaded + 1}.jpg"
                        image_path = os.path.join(SAVE_DIR, image_name)
                        with open(image_path, 'wb') as f:
                            f.write(requests.get(cat_url).content)
                        print(f"Downloaded image {images_downloaded + 1}/{num_images}: {image_path}")
                        images_downloaded += 1
                        if images_downloaded >= num_images:
                            break
                page += 1
            else:
                print("No cat images found")
                break
    except requests.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Download cat images from the cat API")
    parser.add_argument("num_images", type=int, help="Number of cat images to download")
    parser.add_argument("--breed", help="Specify the breed of cat (e.g., siamese)")
    parser.add_argument("--color", help="Specify the color of cat (e.g., black)")
    args = parser.parse_args()

    num_images = args.num_images
    breed = args.breed
    color = args.color

    download_cat_images(num_images, breed, color)


if __name__ == "__main__":
    main()