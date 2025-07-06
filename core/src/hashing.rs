use crate::Article;
use sha2::{Digest, Sha256};
use hex;

/// Generates a SHA-256 hash for the article content
pub fn hash_article(article: &Article) -> String {
    let input = format!(
        "{}:{}:{}:{}:{}",
        article.id, article.title, article.author, article.date, article.content
    );
    let mut hasher = Sha256::new();
    hasher.update(input);
    let result = hasher.finalize();
    hex::encode(result)
}
