# Fonts

Drop your WOFF2 (and WOFF fallback) files here.

## Declare in `assets/css/main.css` or a dedicated `fonts.css`

    @font-face {
        font-family: 'YourFont';
        src: url('../fonts/your-font/YourFont.woff2') format('woff2'),
             url('../fonts/your-font/YourFont.woff')  format('woff');
        font-display: swap;
    }

## Preload in `<head>` of `index.html`

    <link rel="preload" href="assets/fonts/your-font/YourFont.woff2" as="font" type="font/woff2" crossorigin>

Keep the display font local for reliability and performance. Body fonts can use Google Fonts with `preconnect`.
