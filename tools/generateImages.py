from PIL import Image, ImageDraw, ImageFont
import os

# Constants
CARD_WIDTH = 200
CARD_HEIGHT = 300
COLORS = {
    "red": "#E61C23",
    "yellow": "#F9B800",
    "green": "#3FA35B",
    "blue": "#1573D1",
    "black": "#000000"
}
SPECIAL_CARDS = ["skip", "reverse", "+2", "wild", "wild+4"]
ARROWS_IMAGE_PATH = "../uno_cards/arrows.png"  # Arrows image path

def create_base_card(base_color, text, save_path, is_special=False):
    """
    Creates a base UNO card with transparent corners, center ovals, and proper symbols.
    Args:
        base_color (str): Card color.
        text (str): Text or symbol to display.
        save_path (str): File path to save the card image.
        is_special (bool): True for special cards like "skip" or "reverse".
    """
    # Create a blank RGBA card image
    image = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Create a mask for rounded corners
    mask = Image.new("L", (CARD_WIDTH, CARD_HEIGHT), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1],
        radius=20,
        fill=255
    )

    # Draw card background with transparent corners
    card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), base_color)
    image.paste(card, (0, 0), mask)

    # Add white central oval
    oval_margin = 20
    draw.ellipse(
        [oval_margin, CARD_HEIGHT // 4, CARD_WIDTH - oval_margin, CARD_HEIGHT * 3 // 4],
        fill="white"
    )

    # Font setup
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 48)
        font_small = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Text color
    text_color = "black"

    # Draw large central text
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text(
        ((CARD_WIDTH - text_width) // 2, (CARD_HEIGHT - text_height) // 2),
        text, font=font_large, fill=text_color
    )

    # Corner text
    corner_offset = 10
    draw.text((corner_offset, corner_offset), text, font=font_small, fill=text_color)
    draw.text((CARD_WIDTH - text_width - corner_offset, CARD_HEIGHT - text_height - corner_offset),
              text, font=font_small, fill=text_color)

    # Save the card
    image.save(save_path)

def overlay_arrows_on_reverse(card_image_path, save_path):
    """
    Overlays reverse arrows onto a generated UNO reverse card image.
    Args:
        card_image_path (str): Path to the base card image.
        save_path (str): Path to save the final reverse card.
    """
    card_image = Image.open(card_image_path).convert("RGBA")
    arrows_image = Image.open(ARROWS_IMAGE_PATH).convert("RGBA")

    # Resize arrows to fit the card
    arrows_resized = arrows_image.resize((CARD_WIDTH, CARD_HEIGHT))

    # Center position for the arrows
    position = (
        (CARD_WIDTH - arrows_resized.width) // 2,
        (CARD_HEIGHT - arrows_resized.height) // 2
    )

    # Paste arrows onto the card
    card_image.paste(arrows_resized, position, arrows_resized)
    card_image.save(save_path)
    print(f"Reverse card with arrows saved to {save_path}")

def generate_uno_deck(output_folder="uno_cards"):
    """
    Generates a complete UNO card deck with reverse arrows added to reverse cards.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate number cards (0-9 for each color)
    for color_name, color_code in COLORS.items():
        if color_name == "black":
            continue
        for number in range(10):
            file_name = f"{color_name}_{number}.png"
            save_path = os.path.join(output_folder, file_name)
            create_base_card(color_code, str(number), save_path)

    # Generate special cards for each color
    for color_name, color_code in COLORS.items():
        if color_name == "black":
            continue
        for special in ["skip", "reverse", "+2"]:
            file_name = f"{color_name}_{special}.png"
            save_path = os.path.join(output_folder, file_name)
            if special == "reverse":
                create_base_card(color_code, "", save_path)
            else: create_base_card(color_code, special, save_path)

            # If it's a reverse card, overlay the arrows
            if special == "reverse":
                overlay_arrows_on_reverse(save_path, save_path)

    # Generate wild cards (black background)
    for special in ["wild", "wild+4"]:
        file_name = f"{special}.png"
        save_path = os.path.join(output_folder, file_name)
        create_base_card(COLORS["black"], special, save_path)

    print(f"UNO cards generated in folder: {output_folder}")

if __name__ == "__main__":
    generate_uno_deck()
