document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/posts')
        .then(response => response.json())
        .then(data => {
            const blogPosts = data.posts;
            const blogPostsSection = document.getElementById('blog-posts');

            blogPosts.forEach(post => {
                const postElement = document.createElement('article');
                postElement.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <p><i>Posted by ${post.author} on ${post.date}</i></p>
                `;
                blogPostsSection.appendChild(postElement);
            });
        })
        .catch(error => console.error('Error fetching blog posts:', error));
});
