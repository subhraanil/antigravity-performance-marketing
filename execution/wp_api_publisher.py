import requests
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

# The WP REST API usually requires Application Passwords for authentication.
# These can be generated in the WordPress user profile section.
WP_URL = "https://paidmediaworld.com/wp-json/wp/v2"
WP_USERNAME = os.getenv("WP_USERNAME", "subhranil")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# Add cookie to bypass WAF
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Cookie": "humans_21909=1"
}

def upload_image(image_path):
    """Uploads an image to WordPress Media Library."""
    if not WP_APP_PASSWORD:
        print("Error: WP_APP_PASSWORD not found in .env")
        return None
    
    filename = os.path.basename(image_path)
    url = f"{WP_URL}/media"
    
    with open(image_path, "rb") as img:
        headers = {
            **HEADERS,
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "image/png"  # Assuming PNG for now
        }
        response = requests.post(
            url,
            auth=(WP_USERNAME, WP_APP_PASSWORD),
            headers=headers,
            data=img
        )
    
    if response.status_code == 201:
        print(f"Image uploaded successfully: {filename}")
        return response.json()["id"]
    else:
        print(f"Failed to upload image: {response.text}")
        return None

def get_or_create_term(taxonomy, name):
    """Finds a term ID by name or creates it if it doesn't exist."""
    search_url = f"{WP_URL}/{taxonomy}?search={name}"
    # Search for existing term
    search_response = requests.get(search_url, auth=(WP_USERNAME, WP_APP_PASSWORD), headers=HEADERS)
    if search_response.status_code == 200:
        terms = search_response.json()
        for term in terms:
            if term["name"].lower() == name.lower():
                return term["id"]
    
    # If not found, create it
    create_url = f"{WP_URL}/{taxonomy}"
    payload = {"name": name}
    create_response = requests.post(
        create_url, 
        auth=(WP_USERNAME, WP_APP_PASSWORD), 
        headers={**HEADERS, "Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    if create_response.status_code == 201:
        return create_response.json()["id"]
    else:
        # If creation fails (e.g. term already exists but search failed to find it exactly)
        # We might want to try one more search or just return None
        return None

def publish_blog(title, content, slug, category_name=None, tag_names=None, featured_media_id=None):
    """Publishes a blog post to WordPress via REST API."""
    if not WP_APP_PASSWORD:
        print("Error: WP_APP_PASSWORD not found in .env")
        return None

    category_ids = []
    if category_name:
        cat_id = get_or_create_term("categories", category_name)
        if cat_id:
            category_ids.append(cat_id)

    tag_ids = []
    if tag_names:
        for tag_name in tag_names:
            t_id = get_or_create_term("tags", tag_name)
            if t_id:
                tag_ids.append(t_id)

    url = f"{WP_URL}/posts"
    
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "publish",
        "categories": category_ids,
        "tags": tag_ids
    }
    
    if featured_media_id:
        payload["featured_media"] = featured_media_id

    response = requests.post(
        url,
        auth=(WP_USERNAME, WP_APP_PASSWORD),
        headers={
            **HEADERS,
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )

    if response.status_code == 201:
        post_url = response.json()["link"]
        print(f"Post published successfully! URL: {post_url}")
        return post_url
    else:
        print(f"Failed to publish post: {response.text}")
        return None

def get_post_id_by_slug(slug):
    """Finds a post ID by its slug."""
    url = f"{WP_URL}/posts?slug={slug}"
    response = requests.get(url, auth=(WP_USERNAME, WP_APP_PASSWORD), headers=HEADERS)
    if response.status_code == 200:
        posts = response.json()
        if posts:
            return posts[0]["id"]
    return None

def update_blog(post_id, title=None, content=None, slug=None, category_name=None, tag_names=None, featured_media_id=None):
    """Updates an existing blog post via REST API."""
    if not WP_APP_PASSWORD:
        print("Error: WP_APP_PASSWORD not found in .env")
        return None

    payload = {}
    if title:
        payload["title"] = title
    if content:
        payload["content"] = content
    
    if category_name:
        cat_id = get_or_create_term("categories", category_name)
        if cat_id:
            payload["categories"] = [cat_id]

    if slug:
        payload["slug"] = slug

    if tag_names:
        tag_ids = []
        for tag_name in tag_names:
            t_id = get_or_create_term("tags", tag_name)
            if t_id:
                tag_ids.append(t_id)
        if tag_ids:
            payload["tags"] = tag_ids

    if featured_media_id:
        payload["featured_media"] = featured_media_id

    url = f"{WP_URL}/posts/{post_id}"
    
    response = requests.post(
        url,
        auth=(WP_USERNAME, WP_APP_PASSWORD),
        headers={
            **HEADERS,
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        post_url = response.json()["link"]
        print(f"Post updated successfully! URL: {post_url}")
        return post_url
    else:
        print(f"Failed to update post: {response.text}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish or update a blog post via WP REST API")
    parser.add_argument("--title")
    parser.add_argument("--content")
    parser.add_argument("--content-file", help="Path to a file containing the blog content")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--image", help="Path to the featured image")
    parser.add_argument("--category", help="Category name")
    parser.add_argument("--tags", help="Comma-separated tag names")
    parser.add_argument("--new-slug", help="New slug for the post (only used with --update)")
    parser.add_argument("--update", action="store_true", help="Update existing post instead of creating new")
    
    args = parser.parse_args()
    
    content = args.content
    if args.content_file:
        with open(args.content_file, "r", encoding="utf-8") as f:
            content = f.read()

    if not content:
        print("Error: Either --content or --content-file must be provided.")
        exit(1)
    
    if args.update:
        post_id = get_post_id_by_slug(args.slug)
        if post_id:
            media_id = None
            if args.image:
                media_id = upload_image(args.image)
            tag_list = [t.strip() for t in args.tags.split(",")] if args.tags else []
            update_blog(post_id, title=args.title, content=content, slug=args.new_slug, category_name=args.category, tag_names=tag_list, featured_media_id=media_id)
        else:
            print(f"Error: Could not find post with slug '{args.slug}' to update.")
    else:
        media_id = None
        if args.image:
            media_id = upload_image(args.image)
            
        tag_list = [t.strip() for t in args.tags.split(",")] if args.tags else []
            
        publish_blog(
            args.title or "Untitled Post", 
            content, 
            args.slug, 
            category_name=args.category, 
            tag_names=tag_list, 
            featured_media_id=media_id
        )
