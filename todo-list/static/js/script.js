// Подтверждение удаления (опционально)
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="/delete/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Удалить эту задачу? Действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
});

