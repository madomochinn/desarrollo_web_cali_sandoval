// Gráfico de líneas - Avisos por día
Highcharts.chart("graficoLineas", {
    chart: {
      type: "line",
    },
    title: {
      text: "Número de Avisos por Día",
    },
    xAxis: {
      type: "datetime",
      dateTimeLabelFormats: {
        month: "%b %e, %Y",
      },
      title: {
        text: "Fecha",
      },
    },
    yAxis: {
      title: {
        text: "Número de Avisos",
      },
    },
    legend: {
      align: "left",
      verticalAlign: "top",
      borderWidth: 0,
    },
    tooltip: {
      shared: true,
      crosshairs: true,
    },
    series: [
      {
        name: "Avisos",
        data: [],
        lineWidth: 1,
        marker: {
          enabled: true,
          radius: 4,
        },
        color: "#FC2865",
      },
    ],
  });
  
  fetch("/get-stats-avisos-dia")
    .then((response) => response.json())
    .then((data) => {
      let parsedData = data.map((item) => {
        const [year, month, day] = item.date
          .split("-")
          .map((part) => parseInt(part, 10));
        return [
          Date.UTC(year, month - 1, day),
          item.count,
        ];
      });
  
      
      const chart = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id === "graficoLineas"
      );
  
      // actualizar
      chart.update({
        series: [
          {
            data: parsedData,
          },
        ],
      });
    })
    .catch((error) => console.error("Error:", error));
  
  // Gráfico de torta - Avisos por tipo
  Highcharts.chart("graficoTorta", {
    chart: {
      type: "pie",
    },
    title: {
      text: "Distribución por Tipo de Mascota",
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b>: {point.y}'
        }
      }
    },
    series: [
      {
        name: "Avisos",
        data: [],
        colorByPoint: true,
      },
    ],
  });
  
  fetch("/get-stats-avisos-tipo")
    .then((response) => response.json())
    .then((data) => {
      const seriesData = data.map(item => ({
        name: item.tipo === 'perro' ? 'Perros' : 'Gatos',
        y: item.count
      }));
  
      const chart = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id === "graficoTorta"
      );
  
      // actualizar
      chart.update({
        series: [
          {
            data: seriesData,
          },
        ],
      });
    })
    .catch((error) => console.error("Error:", error));
  
  // Gráfico de barras - Avisos por mes y tipo
  Highcharts.chart("graficoBarras", {
    chart: {
      type: "column",
    },
    title: {
      text: "Avisos por Mes y Tipo",
    },
    xAxis: {
      categories: [],
      crosshair: true,
    },
    yAxis: {
      title: {
        text: "Cantidad de Avisos",
      },
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y}</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0
      }
    },
    series: [
      {
        name: "Perros",
        data: [],
        color: "#FF6384"
      },
      {
        name: "Gatos", 
        data: [],
        color: "#36A2EB"
      }
    ],
  });
  
  fetch("/get-stats-avisos-mes")
    .then((response) => response.json())
    .then((data) => {
      // Agrupar datos por mes
      const datosAgrupados = {};
      
      data.forEach(item => {
        const clave = `${item.año}-${item.mes}`;
        const nombreMes = obtenerNombreMes(item.mes);
        const label = `${nombreMes} ${item.año}`;
        
        if (!datosAgrupados[clave]) {
          datosAgrupados[clave] = {
            label: label,
            perros: 0,
            gatos: 0
          };
        }
        
        if (item.tipo === 'perro') {
          datosAgrupados[clave].perros = item.count;
        } else {
          datosAgrupados[clave].gatos = item.count;
        }
      });
  
      const categorias = Object.values(datosAgrupados).map(item => item.label);
      const datosPerros = Object.values(datosAgrupados).map(item => item.perros);
      const datosGatos = Object.values(datosAgrupados).map(item => item.gatos);
  
      const chart = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id === "graficoBarras"
      );
  
      // actualizar
      chart.update({
        xAxis: {
          categories: categorias
        },
        series: [
          {
            data: datosPerros,
          },
          {
            data: datosGatos,
          }
        ],
      });
    })
    .catch((error) => console.error("Error:", error));
  
  // Función auxiliar para obtener nombre del mes
  function obtenerNombreMes(numeroMes) {
    const meses = [
      'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ];
    return meses[numeroMes - 1];
  }