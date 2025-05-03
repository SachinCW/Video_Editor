import os
from PIL import Image, ImageDraw, ImageFont

def draw_text(draw, text, position, font, max_width, line_spacing):
    # Initialize variables
    lines = []
    words = text.split()

    # Word wrapping
    while words:
        line = ''
        while words and draw.textbbox((position[0], 0), line + words[0], font=font)[2] <= max_width:
            line = line + (words.pop(0) + ' ')
        lines.append(line)

    # Calculate line height for spacing
    line_height = draw.textbbox((position[0], position[1]), 'A', font=font)[3] - draw.textbbox((position[0], position[1]), 'A', font=font)[1]

    # Draw lines on image with consistent line spacing
    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill="#dddddd")  # Updated text color to #dddddd
        y += line_height + line_spacing  # Apply consistent spacing

def update_thumbnail(video_name, thumbnail_path='base_thumbnail.png', output_path='updated_thumbnail.jpg', font_path='/Library/Fonts/Arial Bold.ttf'):
    # Open the image
    img = Image.open(thumbnail_path).convert("RGB")  # Convert to RGB to remove alpha channel

    # Get a font (Arial Bold)
    font_size = 60  # Adjust font size as needed
    font = ImageFont.truetype(font_path, font_size)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Define text position, maximum width, and line spacing
    text_position_x = 100  # Adjust horizontal position as needed
    text_position_y = int(img.height * 0.18)  # Start printing 15% below the top of the image
    max_width = img.width - text_position_x - 50  # Adjust max width as needed
    line_spacing = 50  # Adjust line spacing as needed

    # Add text to image with word wrapping
    draw_text(draw, video_name, (text_position_x, text_position_y), font, max_width, line_spacing)

    # Save the image
    img.save(output_path, "JPEG")

def generate_thumbnails(captions_dir, thumbnails_dir, base_thumbnail_path, font_path):
    # Ensure the output directory exists
    if not os.path.exists(thumbnails_dir):
        os.makedirs(thumbnails_dir)

    # Iterate over all .srt files in the captions directory
    for filename in os.listdir(captions_dir):
        if filename.endswith('.srt'):
            # Extract the sequencing prefix and the video name
            parts = filename.split()
            sequencing_prefix = parts[0]  # Get the sequencing prefix (e.g., "1.1")
            video_name = ' '.join(parts[1:]).replace('.srt', '').replace('ALTERED', '').strip()
            
            # Generate the thumbnail file name with sequencing
            output_path = os.path.join(thumbnails_dir, f"{sequencing_prefix} {video_name}.jpg")
            
            # Update the thumbnail
            update_thumbnail(video_name, thumbnail_path=base_thumbnail_path, output_path=output_path, font_path=font_path)

if __name__ == "__main__":
    captions_dir = '/Users/sachin/Data/G/Data Engineering Hub/AWS Data Engineering BootCamp/Deep Dive Captions'
    thumbnails_dir = '/Users/sachin/Data/G/Data Engineering Hub/AWS Data Engineering BootCamp/Deep Dive Thumbnails'
    base_thumbnail_path = 'base_thumbnail.png'  # This should be in the same directory as your script.
    font_path = '/Library/Fonts/Arial Bold.ttf'  # Path to Arial Bold font on your Mac.

    generate_thumbnails(captions_dir, thumbnails_dir, base_thumbnail_path, font_path)
