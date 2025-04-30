document.addEventListener('DOMContentLoaded', () => {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const filter = searchInput.value.toLowerCase();
            document.querySelectorAll('#articles .card').forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const summary = card.querySelector('p').textContent.toLowerCase();
                
                if (title.includes(filter) || summary.includes(filter)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Category filtering
    const categoryButtons = document.querySelectorAll('.category-filter');
    if (categoryButtons.length) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                categoryButtons.forEach(btn => {
                    btn.classList.remove('active', 'bg-[#ffd502]', 'text-gray-900');
                    btn.classList.add('bg-gray-200', 'text-gray-700');
                });
                
                // Add active class to clicked button
                this.classList.add('active', 'bg-[#ffd502]', 'text-gray-900');
                this.classList.remove('bg-gray-200', 'text-gray-700');
                
                const category = this.dataset.category;
                
                // Filter articles
                document.querySelectorAll('#articles .card').forEach(card => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // Animated buttons
    const editButtons = document.querySelectorAll('.edit-btn');
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    editButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.classList.add('animate-wiggle');
        });
        
        button.addEventListener('mouseout', function() {
            this.classList.remove('animate-wiggle');
        });
    });
    
    deleteButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.classList.add('animate-shake');
        });
        
        button.addEventListener('mouseout', function() {
            this.classList.remove('animate-shake');
        });
    });
    
    // Fade-in animation for articles
    const articles = document.querySelectorAll('.article-card');
    articles.forEach((article, index) => {
        article.style.opacity = '0';
        article.style.transform = 'translateY(20px)';
        article.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            article.style.opacity = '1';
            article.style.transform = 'translateY(0)';
        }, 100 * index);
    });
});