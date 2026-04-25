/* GLOBAL VARIABLES */
bookCatalog = []; 
bookCategories = [];

shoppingCart = [];

/* FUNCTION DEFINITIONS */
function getJsonObject(path, success, error) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                if (success) success(JSON.parse(xhr.responseText));
            } else {
                if (error) error(xhr);
            }
        }
    };
    xhr.open("GET", path, true);
    xhr.send();
}

function populateCatalog(data) {
    const tableBody = document.querySelector("#bookTable tbody");
    tableBody.innerHTML = '';

    if (!data || data.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 9; // Number of columns in your table
        cell.textContent = "There are no results.";
        cell.style.textAlign = "center";
        cell.style.fontStyle = "italic";

        row.appendChild(cell);
        tableBody.appendChild(row);
    } else {
        data.forEach(item => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td><input type="checkbox" class="radioCheck" name="selectedBook" onclick='check(this);' data-index="${bookCatalog.indexOf(item)}"/></td>
                <td><img src=${item.img} alt="Cover" class="book-cover" /></td>
                <td class="book-title">${item.title}</td>
                <td>${convertRatingToStars(Number(item.rating))}</td>
                <td>${item.authors}</td>
                <td>${item.year}</td>
                <td>${item.price}</td>
                <td>${item.publisher}</td>
                <td>${item.category}</td>
            `;

            tableBody.appendChild(row);
        })
    }
}

function check(input) {
    let checkboxes = document.getElementsByClassName("radioCheck");
    for (let i = 0; i < checkboxes.length; i++) {
        if(checkboxes[i].checked == true) {
            checkboxes[i].checked = false;
        }
    }
    
    if (input.checked == true) {
        input.checked = false;
    } else {
        input.checked = true;
    }	
}

function convertRatingToStars(rating) {
    if (typeof(rating) != "number") throw new TypeError();
    if (rating < 0 || rating > 5) throw new Error("Rating must be between 0 and 5");

    let html = '<div class="rating-column-entry">';
    for (let i = 0; i < rating; i++) {
        html += '<img src="images/star-16.ico" alt="star"/>';
    }
    for (let i = 0; i < 5 - rating; i++) {
        html += '<img src="images/outline-star-16.ico" alt="outline star"/>';
    }
    html += '</div>';

    return html;
}

function populateCategoryFilter(data) {
    data.forEach(item => {
        if (!bookCategories.includes(item.category)) {
            bookCategories.push(item.category);
        }
    })

    const dropdown = document.getElementById('filterCategory');

    const defaultOption = document.createElement('option');
    defaultOption.value = 'all';
    defaultOption.textContent = 'All Categories';
    dropdown.appendChild(defaultOption);

    bookCategories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        dropdown.appendChild(option);
    });

    const boundaryTesting = document.createElement('option');
    boundaryTesting.value = '';
    boundaryTesting.textContent = 'Music (TESTING)';
    dropdown.appendChild(boundaryTesting);
}

function applyFilter(category) {
    if (category === "all") {
        populateCatalog(bookCatalog)
    } else if (!bookCategories.includes(category)) {
        populateCatalog();
        alert("There are no books which match that category!");
    } else {
        const filtered = bookCatalog.filter(book => book.category === category);
        populateCatalog(filtered);
    }
}

function search(searchString) {
    if (!searchString || searchString.length == 0) {
        const tableRows = document.querySelectorAll("#bookTable tbody tr");
        tableRows.forEach(row => {
            row.classList.remove("highlight");
        })
        return
    }

    const titleElements = document.querySelectorAll("#bookTable tbody .book-title");

    let numMatches = 0;
    titleElements.forEach(titleEl => {
        const row = titleEl.closest("tr"); // get the full row
        const title = titleEl.innerText.toLowerCase();
        const match = title.includes(searchString.toLowerCase());

        if (match) {
            row.classList.add("highlight");
            numMatches++;
        } else {
            row.classList.remove("highlight");
        }
    });

    if (numMatches == 0) {
        alert("Your search did not match any results!");
    }
}

function getSelectedBook() {
    const selectedRadio = document.querySelector('input[name="selectedBook"]:checked');
    if (!selectedRadio) {
        alert("No book selected.");
        return null;
    }

    const index = selectedRadio.getAttribute('data-index');
    const book = bookCatalog[Number(index)];
    return book;
}

function updateCartTotal() {
    const cartTotal = document.getElementById("cartTotal");
    cartTotal.innerText = shoppingCart.length;
}

function addToCart() {
    const book = getSelectedBook();
    if (!book) return; // No book selected

    const input = prompt("How many do you wish to add to cart?", "Number of copies");

    if (input === null || input.trim() === "") return; // User cancelled or empty input

    const numBooks = Number(input);
    if (Number.isNaN(numBooks) || numBooks <= 0 || numBooks > 1000) {
        alert("Please enter a valid positive number less than 1000.");
        return;
    }

    for (let i = 0; i < numBooks; i++) {
        shoppingCart.push(book);
    }

    updateCartTotal();
}

function resetCart() {
    let resetMessage = "Are you sure you want to reset the cart?";
    if (confirm(resetMessage)) {
        shoppingCart = [];
        updateCartTotal();
    } 
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

function resetAllFilters() {
    search();
    applyFilter("all");
    document.getElementById("searchInput").value = "";
    document.getElementById("filterCategory").value = "all";
}

function onError(xhr) {
    console.error(xhr);
}

function onDataLoad(data) {
    bookCatalog = data; 
    console.log(bookCatalog);

    populateCatalog(bookCatalog);
    populateCategoryFilter(bookCatalog);

    const searchBar = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const filterCategory = document.getElementById("filterCategory");
    const filterButton = document.getElementById("filterButton");
    const resetAllButton = document.getElementById("resetAllButton");
    const darkModeButton = document.getElementById("darkModeButton");
    const addToCartButton = document.getElementById("addToCartButton");
    const resetCartButton = document.getElementById("resetCartButton");

    searchButton.onclick = () => search(searchBar.value);
    filterButton.onclick = () => applyFilter(filterCategory.value);
    resetAllButton.onclick = resetAllFilters;
    darkModeButton.onclick = toggleDarkMode;
    addToCartButton.onclick = addToCart;
    resetCartButton.onclick = resetCart;
}

window.onload = function() {
    getJsonObject('data.json', onDataLoad, onError);
}