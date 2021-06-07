const colors = require("tailwindcss/colors");

module.exports = {
    mode: "jit",
    theme: {
        extend: {
            colors: {
                gray: colors.gray,
                orange: colors.orange,
                rose: colors.rose,
            },
        },
    },
    purge: ["./**/*.{html,py}"],
    plugins: [],
    darkMode: "media", // class or media
};
