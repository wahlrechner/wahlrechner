const colors = require("tailwindcss/colors");

module.exports = {
    purge: ["wahlrechner/**/*.{html,py}"],
    theme: {
        extend: {},
        colors: {
            transparent: "transparent",
            current: "currentColor",
            white: "white",
            gray: colors.gray,
            red: colors.red,
            yellow: colors.amber,
            green: colors.emerald,
            blue: colors.blue,
            indigo: colors.indigo,
            purple: colors.violet,
            pink: colors.pink,
        },
    },
    variants: {},
    plugins: [],
    darkMode: "media",
};
