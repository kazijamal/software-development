// Cache JSON and CSV files into localStorage
const cacheData = (key, filePath, extension) => {
    const cachedData = JSON.parse(localStorage.getItem(key));

    if (!cachedData) {
        switch (extension) {
            case "JSON":
                d3.json(filePath)
                    .then((json) => {
                        localStorage.setItem(key, JSON.stringify(json));
                    })
                    .catch((err) => {
                        console.log(err);
                    });
                break;
            // case "CSV":
            //     d3.csv(filePath)
            //         .then((csv) => {
            //             localStorage.setItem(key, JSON.stringify(csv));
            //         })
            //         .catch((err) => {
            //             console.log(err);
            //         });
            //     break;
            default:
                break;
        }
    }
};

export default cacheData;