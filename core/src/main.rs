use std::fs;
use std::path::Path;
use serde_json;

mod hashing;
mod lib;

use crate::hashing::hash_article;
use lib::Article; // ← your struct

fn main() {
    let path = Path::new("../articles.json");

    let data = fs::read_to_string(&path)
        .expect("Failed to read ../articles.json");

    let mut articles: Vec<Article> = serde_json::from_str(&data)
        .expect("Failed to parse JSON");

    for (i, article) in articles.iter_mut().enumerate() {
        let hash = hash_article(&article);
        article.hash = hash.clone(); // ✅ inject hash into the struct
        println!("✅ Article [{}]: '{}' → Hash: {}", i + 1, article.title, hash);
    }

    // ✅ Write back the updated list
    let updated_json = serde_json::to_string_pretty(&articles)
        .expect("Failed to serialize updated articles");
    fs::write(&path, updated_json)
        .expect("Failed to write updated articles with hashes");
}
