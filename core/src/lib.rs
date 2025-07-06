use serde::{Deserialize, Serialize};
use std::collections::hash_map::DefaultHasher;
use std::fs;
use std::hash::{Hash, Hasher};
use std::io::Read;
use std::path::Path;

/// Ensure strict data handling — article schema with full fields
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Article {
    #[serde(default)]
    pub id: usize,

    #[serde(default)]
    pub hash: String,

    pub title: String,
    pub author: String,
    pub date: String,
    pub content: String,
}

/// Load JSON from string and return an Article (input comes from Python)
pub fn parse_article_json(json_data: &str) -> Result<Article, Box<dyn std::error::Error>> {
    assert!(!json_data.trim().is_empty(), "Empty JSON input not allowed.");
    let mut article: Article = serde_json::from_str(json_data)?;
    validate_article_fields(&article)?;

    // Compute article hash
    let mut hasher = DefaultHasher::new();
    article.title.hash(&mut hasher);
    article.author.hash(&mut hasher);
    article.date.hash(&mut hasher);
    article.content.hash(&mut hasher);
    article.hash = format!("{:x}", hasher.finish());

    Ok(article)
}

/// Simple validator for article completeness — NASA-safe assertions
fn validate_article_fields(article: &Article) -> Result<(), &'static str> {
    if article.title.trim().is_empty()
        || article.author.trim().is_empty()
        || article.date.trim().is_empty()
        || article.content.trim().is_empty()
    {
        return Err("Invalid article: One or more fields are empty.");
    }
    Ok(())
}

/// Store the article in `articles.json` with unique ID and hash tracking
pub fn save_article(article: Article, file_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let path = Path::new(file_path);
    let mut articles: Vec<Article> = if path.exists() {
        let mut content = String::new();
        fs::File::open(path)?.read_to_string(&mut content)?;
        serde_json::from_str(&content)?
    } else {
        vec![]
    };

    // Prevent duplicates via hash
    if articles.iter().any(|a| a.hash == article.hash) {
        println!("⚠️  Duplicate detected. Skipping article: '{}'", article.title);
        return Ok(()); // Exit cleanly
    }

    let mut article = article;
    article.id = articles.len() + 1;

    println!(
        "✅ Article [{}]: '{}' → Hash: {}",
        article.id, article.title, article.hash
    );

    articles.push(article);
    let serialized = serde_json::to_string_pretty(&articles)?;
    fs::write(path, serialized)?;

    Ok(())
}
