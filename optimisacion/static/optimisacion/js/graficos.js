    const fechasHoras = JSON.parse('{{ fechas_horas|escapejs }}');
    const consumos = JSON.parse('{{ consumos|escapejs }}');
    const dispositivo = '{{ dispositivo|escapejs }}';
    const registroId = '{{ registro_id|escapejs }}';
    const maximo = parseFloat('{{ maximo|escapejs }}');
    const minimo = parseFloat('{{ minimo|escapejs }}');


    const ctx = document.getElementById('consumoChart').getContext('2d');
    const consumoChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: fechasHoras,
            datasets: [{
                label: `Consumo eléctrico ${dispositivo}`,
                data: consumos,
                fill: false,
                borderColor: 'rgb(192, 75, 75)',
                tension: 0.1
            },
            {
                label: `Máximo (${maximo} kWh)`,
                data: Array(fechasHoras.length).fill(maximo), // Crea un array lleno del valor máximo
                fill: false,
                borderColor: 'rgb(54, 162, 235)',
                borderDash: [5, 5], // Línea punteada para diferenciar
                pointRadius: 0, // Oculta los puntos
                tension: 0
            },
            {
                label: `Mínimo (${minimo} kWh)`,
                data: Array(fechasHoras.length).fill(minimo), // Crea un array lleno del valor mínimo
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                borderDash: [5, 5], // Línea punteada para diferenciar
                pointRadius: 0, // Oculta los puntos
                tension: 0
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Consumo eléctrico (kWh)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Fecha y Hora'
                    },
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10 // Adjust as needed
                    },
                    adapters: {
                        date: {
                            format: 'YYYY-MM-DD HH:mm'
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            return tooltipItems[0].label;
                        },
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'decimal' }).format(context.parsed.y);
                            }
                            return label + ' kWh';
                        }
                    }
                }
            }
        }
    });

    //Gráfico circular de distribución por dispositivo
    const pieLabels = JSON.parse('{{ pie_chart_labels|escapejs }}');
    const pieData = JSON.parse('{{ pie_chart_data|escapejs }}');

    const pieCtx = document.getElementById('pieChart').getContext('2d');
    const pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                label: 'Distribución de dispositivos',
                data: pieData,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#8e5ea2', '#3cba9f', '#e8c3b9', '#c45850'
                ],
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            return `${label}: ${value} registros`;
                        }
                    }
                }
            }
        }
    });

    // Gráfico de líneas múltiples
    const multiLabels = JSON.parse('{{ lineas_multiples_labels|escapejs }}');
    const multiSeries = JSON.parse('{{ lineas_multiples_series|escapejs }}');

    const multiDatasets = Object.keys(multiSeries).map((dispositivo, index) => {
        const colors = [
            'rgb(255, 99, 132)', 'rgb(54, 162, 235)',
            'rgb(255, 206, 86)', 'rgb(75, 192, 192)',
            'rgb(153, 102, 255)', 'rgb(255, 159, 64)'
        ];
        return {
            label: dispositivo,
            data: multiSeries[dispositivo],
            borderColor: colors[index % colors.length],
            fill: false,
            tension: 0.1
        };
    });

    const multiCtx = document.getElementById('multiLineChart').getContext('2d');
    const multiLineChart = new Chart(multiCtx, {
        type: 'line',
        data: {
            labels: multiLabels,
            datasets: multiDatasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Consumo por Dispositivo'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                },
                legend: {
                    position: 'bottom'
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Consumo (kWh)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Fecha y Hora'
                    }
                }
            }
        }
    });
