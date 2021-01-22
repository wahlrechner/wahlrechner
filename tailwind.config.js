const colors = require("tailwindcss/colors");

module.exports = {
    purge: ["wahlrechner/**/*.{html,py}"],
    theme: {
        extend: {
            colors: {
                gray: colors.gray,
            },
        },
    },
    variants: {},
    plugins: [],
    darkMode: "class",
};
