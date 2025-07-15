import json
from pathlib import Path

from django.core.files import File
from django.conf import settings

# --- Import your models ---
from sneakers.models import Brand, Sneaker

def run():
    """
    This script is executed by running: 'python manage.py runscript seed_data'
    It replaces all database data with test data for development.
    """
    if not settings.DEBUG:
        print("Seeding is only allowed in DEBUG mode.")
        return

    confirm = input('Replace all existing data with test data? This cannot be undone. (y/n): ')
    if confirm.lower() != 'y':
        print("Seeding cancelled.")
        return

    # Setup Paths
    script_dir = Path(__file__).parent
    brand_data_path = script_dir / "brands.json"
    sneaker_data_path = script_dir / "sneakers.json"
    image_dir_path = script_dir / "seed_images"

    if not all([brand_data_path.exists(), sneaker_data_path.exists()]):
        print("Ensure brands.json and sneakers.json exist in the scripts directory.")
        return

    # Clear existing objects
    print("Deleting existing data...")
    Sneaker.objects.all().delete()
    Brand.objects.all().delete()

    # Load and create brand data
    print("Creating brands...")
    with open(brand_data_path, "r", encoding="utf-8") as f:
        brand_data = json.load(f)
        for brand_item in brand_data:
            Brand.objects.create(**brand_item)
    print(f"{Brand.objects.count()} brands created.")

    # Load sneaker data
    with open(sneaker_data_path, "r", encoding="utf-8") as f:
        sneaker_data = json.load(f)

    # Create Sneaker Objects
    print("Creating sneakers...")
    sneaker_objects_map = {}
    for sneaker_item in sneaker_data:
        try:
            brand_name = sneaker_item.pop("brand_name")
            brand_instance = Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            print(f"Brand '{brand_name}' not found. Skipping sneaker '{sneaker_item['name']}'.")
            continue
        except KeyError:
            print(f"'brand_name' missing for sneaker '{sneaker_item['name']}'. Skipping.")
            continue

        related_names = sneaker_item.pop("related_sneakers", [])
        image_filename = sneaker_item.pop("primary_image", None)

        new_sneaker = Sneaker.objects.create(brand=brand_instance, **sneaker_item)

        if image_filename:
            image_path = image_dir_path / image_filename

            print(f"\nProcessing sneaker: {new_sneaker.name}")
            print(f"  > Looking for image: {image_filename}")
            print(f"  > Expecting it at full path: {image_path.resolve()}")

            if image_path.exists():
                with open(image_path, "rb") as img_f:
                    new_sneaker.primary_image.save(image_filename, File(img_f), save=True)
            else:
                print(f"Image not found: {image_path}")

        sneaker_objects_map[new_sneaker.name] = {
            "instance": new_sneaker,
            "related_names": related_names
        }
    print(f"{Sneaker.objects.count()} sneakers created.")

    # Add Many-to-Many relationships
    print("Adding relationships...")
    for name, data in sneaker_objects_map.items():
        sneaker_instance = data["instance"]
        related_names = data["related_names"]
        if not related_names:
            continue
        
        related_instances = [sneaker_objects_map[r_name]["instance"] for r_name in related_names if r_name in sneaker_objects_map]
        sneaker_instance.related_sneakers.set(related_instances)
    print("Relationships added.")

    print("\nDatabase seeded successfully.")