#!/usr/bin/env python3
"""
Update image paths in HTML files from Flickr URLs to local paths.
"""

import re
import os
from pathlib import Path


def extract_img_number(alt_text):
    """Extract the number from alt text like 'IMG_2055'."""
    match = re.search(r'IMG_(\d+)', alt_text)
    return match.group(1) if match else None


def process_html_file(file_path, is_main_file=False):
    """
    Process a single HTML file, replacing Flickr URLs with local paths.
    
    Args:
        file_path: Path to the HTML file
        is_main_file: True if this is pics.html, False for p2-p6.html files
    
    Returns:
        Tuple of (processed_img_numbers, replacement_count)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    processed_numbers = set()
    replacement_count = 0
    
    # Determine the relative path prefix
    path_prefix = 'pics/' if is_main_file else '../pics/'
    
    # Pattern to match anchor tags containing img tags with alt="IMG_XXXX"
    # This pattern captures the entire anchor block with the img tag inside
    pattern = r'<a\s+([^>]*href=")[^"]*("[^>]*)>\s*<img\s+([^>]*alt="IMG_\d+"[^>]*)>\s*</a>'
    
    def replace_urls(match):
        nonlocal replacement_count, processed_numbers
        
        # Extract the parts
        before_href = match.group(1)  # '<a ...href="'
        after_href = match.group(2)   # '" ...>'
        img_attrs = match.group(3)     # 'img attributes including alt="IMG_XXXX"'
        
        # Extract IMG number from alt attribute
        alt_match = re.search(r'alt="IMG_(\d+)"', img_attrs)
        if not alt_match:
            return match.group(0)  # Return unchanged if no number found
        
        img_number = alt_match.group(1)
        processed_numbers.add(img_number)
        
        # Replace the href URL in anchor tag
        new_href_url = f'{path_prefix}full/img_{img_number}_1600.jpg'
        
        # Replace the src URL in img tag
        new_src_url = f'{path_prefix}thumbs/img_{img_number}_320.jpg'
        
        # Update img src attribute
        img_attrs_updated = re.sub(
            r'src="[^"]*"',
            f'src="{new_src_url}"',
            img_attrs
        )
        
        # Reconstruct the anchor tag with updated URLs
        new_tag = f'<a {before_href}{new_href_url}{after_href}><img {img_attrs_updated}></a>'
        
        replacement_count += 1
        return new_tag
    
    # Replace all matching patterns
    content = re.sub(pattern, replace_urls, content, flags=re.DOTALL)
    
    # Also handle img tags that might have src before alt or different ordering
    # This is a more flexible pattern that handles img tags within anchor tags
    # regardless of attribute order
    pattern2 = r'<a\s+([^>]*)href="[^"]*"([^>]*)>\s*<img\s+([^>]*)>\s*</a>'
    
    def replace_urls_flexible(match):
        nonlocal replacement_count, processed_numbers
        
        anchor_attrs_before = match.group(1)
        anchor_attrs_after = match.group(2)
        img_attrs = match.group(3)
        
        # Check if this img has alt="IMG_XXXX"
        alt_match = re.search(r'alt="IMG_(\d+)"', img_attrs)
        if not alt_match:
            return match.group(0)  # Return unchanged
        
        img_number = alt_match.group(1)
        
        # Check if already processed (by previous pattern)
        full_match = match.group(0)
        if img_number in processed_numbers and f'img_{img_number}_' in full_match:
            return match.group(0)  # Already updated
        
        processed_numbers.add(img_number)
        
        # Replace the href URL
        new_href_url = f'{path_prefix}full/img_{img_number}_1600.jpg'
        new_anchor_before = re.sub(r'href="[^"]*"', f'href="{new_href_url}"', anchor_attrs_before)
        if new_anchor_before == anchor_attrs_before:
            # href wasn't in the before part, must be in after part
            new_anchor_after = re.sub(r'href="[^"]*"', f'href="{new_href_url}"', anchor_attrs_after)
        else:
            new_anchor_after = anchor_attrs_after
        
        # Replace the src URL in img tag
        new_src_url = f'{path_prefix}thumbs/img_{img_number}_320.jpg'
        img_attrs_updated = re.sub(r'src="[^"]*"', f'src="{new_src_url}"', img_attrs)
        
        # Reconstruct the tag
        new_tag = f'<a {new_anchor_before}href="{new_href_url}"{new_anchor_after}><img {img_attrs_updated}></a>'
        
        replacement_count += 1
        return new_tag
    
    # Only apply if the first pattern didn't make changes
    if content == original_content:
        content = re.sub(pattern2, replace_urls_flexible, content, flags=re.DOTALL)
    
    # Write back to file if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return processed_numbers, replacement_count


def main():
    """Main function to process all HTML files."""
    base_dir = Path(__file__).parent
    
    # Define the files to process
    files_to_process = [
        ('pics.html', True),  # (filename, is_main_file)
        ('pics/p2.html', False),
        ('pics/p3.html', False),
        ('pics/p4.html', False),
        ('pics/p5.html', False),
        ('pics/p6.html', False),
    ]
    
    all_processed_numbers = set()
    total_replacements = 0
    summary = []
    
    print("Processing HTML files to replace Flickr URLs with local paths...\n")
    
    for filename, is_main_file in files_to_process:
        file_path = base_dir / filename
        
        if not file_path.exists():
            print(f"⚠️  File not found: {filename}")
            summary.append(f"{filename}: NOT FOUND")
            continue
        
        try:
            processed_numbers, replacement_count = process_html_file(
                file_path, is_main_file
            )
            
            all_processed_numbers.update(processed_numbers)
            total_replacements += replacement_count
            
            status = f"✓ {filename}: {replacement_count} replacements, {len(processed_numbers)} unique images"
            print(status)
            summary.append(status)
            
        except Exception as e:
            error_msg = f"✗ {filename}: ERROR - {str(e)}"
            print(error_msg)
            summary.append(error_msg)
    
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"  Total files processed: {len([s for s in summary if '✓' in s])}")
    print(f"  Total replacements made: {total_replacements}")
    print(f"  Unique IMG numbers processed: {len(all_processed_numbers)}")
    
    if all_processed_numbers:
        sorted_numbers = sorted(all_processed_numbers, key=int)
        print(f"  IMG numbers: {', '.join(sorted_numbers)}")
    
    print(f"{'='*70}\n")
    
    return summary


if __name__ == '__main__':
    main()
