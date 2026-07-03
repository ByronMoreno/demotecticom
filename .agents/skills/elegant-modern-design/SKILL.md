---
name: elegant-modern-design
description: Directrices y estilos para crear diseños de aplicaciones web elegantes, modernos y premium con paletas de colores sofisticadas, tipografía fina, animaciones sutiles y efectos de glassmorfismo.
---

# Premium & Modern Design Guidelines

Este skill define las directrices y estándares para el diseño visual de interfaces web premium, asegurando que cada aplicación luzca profesional, limpia y visualmente impresionante.

## 🎨 Paleta de Colores Sofisticada
Evitar colores primarios saturados por defecto. Usar paletas de color con armonía visual basadas en tonos HSL, grises fríos y gradientes suaves.

### Tema Oscuro Premium (Deep Space)
- **Fondo Principal**: `#0b0f19` (Gris oscuro azulado profundo)
- **Fondo de Contenedores**: `rgba(22, 30, 49, 0.7)`
- **Bordes y Divisiones**: `rgba(255, 255, 255, 0.08)`
- **Texto Principal**: `#f8fafc` (Slate 50)
- **Texto Secundario**: `#94a3b8` (Slate 400)
- **Acento Primario**: `linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)` (Indigo)
- **Acento Secundario**: `linear-gradient(135deg, #ec4899 0%, #be185d 100%)` (Rosa/Magenta)

### Tema Claro Premium (Alabaster Glass)
- **Fondo Principal**: `#f8fafc` (Slate 50)
- **Fondo de Contenedores**: `rgba(255, 255, 255, 0.7)`
- **Bordes y Divisiones**: `rgba(0, 0, 0, 0.06)`
- **Texto Principal**: `#0f172a` (Slate 900)
- **Texto Secundario**: `#64748b` (Slate 500)

---

## 🪟 Efecto de Glassmorfismo (Glassmorphism)
Para lograr un efecto moderno y tridimensional, los contenedores y tarjetas deben usar fondos translúcidos con desenfoque de fondo.

### Clase CSS Estándar:
```css
.glass-card {
    background: rgba(22, 30, 49, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
```

---

## ✍️ Tipografía Fina
No utilizar fuentes predeterminadas del navegador. Utilizar fuentes premium y modernas de Google Fonts:
- **Inter**: Para interfaces limpias y de alta legibilidad técnica.
- **Outfit** o **Plus Jakarta Sans**: Para un aspecto moderno, geométrico y elegante.
- **Playfair Display**: Para encabezados elegantes o literarios.

### Configuración:
```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    letter-spacing: -0.01em;
}
```

---

## 🔄 Micro-animaciones y Efectos Hover
Los elementos interactivos deben sentirse vivos y responder suavemente al usuario.

### Transición Suave Global:
`transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);`

### Hover en Tarjetas:
```css
.card-interactive {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-interactive:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.4);
}
```

### Animación de Entrada (Fade In):
```css
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.animate-slide-up {
    animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

---

## 🗂️ Diseño de Botones y Formularios Premium
- **Botones con Gradiente y Sombra**: Los botones de acción principal deben usar gradientes suaves con una sombra del mismo tono que se difumina.
- **Inputs Minimalistas**: Bordes finos, fondos oscuros semitransparentes y foco con anillo de luz suave.

```css
.btn-premium {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}
.btn-premium:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45);
}

.input-premium {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    color: #f8fafc;
}
.input-premium:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
}
```
