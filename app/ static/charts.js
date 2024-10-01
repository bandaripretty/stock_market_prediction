document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/stock/AAPL')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(entry => entry.date);
            const prices = data.map(entry => entry.close);

            const ctx = document.getElementById('priceChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'AAPL Stock Price',
                        data: prices,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            }
                        },
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        });
});
