const colors = require("tailwindcss/colors");

module.exports = {
    mode: "jit",
    content: ["../**/*.{html,py}"],
    plugins: [],
    darkMode: "media", // class or media
    theme: {
        extend: {
            colors: {
                gray: colors.neutral,
            },
        },
    },
};
