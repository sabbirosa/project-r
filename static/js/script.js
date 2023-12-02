var $j = jQuery.noConflict();

document.addEventListener('DOMContentLoaded', function () {
    let diseaseFieldCount = 1;

    window.addDiseaseField = function () {
        const container = document.getElementById('disease-fields');
        const newField = document.createElement('div');
        newField.innerHTML = `
        <div class="disease-field">
            <input type="text" name="blood_diseases_${diseaseFieldCount}" class="disease-input" placeholder="Enter blood disease" >
            <button class="del-btn" type="button" onclick="removeDiseaseField(this.parentElement)"><i class="bi bi-x-square"></i></button>
        </div> 
        `;
        container.appendChild(newField);
        initializeDiseaseAutocomplete(newField.querySelector('.disease-input'));

        diseaseFieldCount++;
    };

    window.addDiseaseFieldOnUserEdit = function () {
        const container = document.getElementById('disease-fields');
        const newField = document.createElement('div');
        newField.innerHTML = `
        <div class="disease-field">
            <input type="text" name="blood_diseases_${diseaseFieldCount}" class="disease-input" placeholder="Enter blood disease" value="">
            <button class="del-btn" type="button" onclick="removeDiseaseField(this.parentElement)"><i class="bi bi-x-square"></i></button>
        </div> 
        `;
        container.querySelector('.add-new-diseases').appendChild(newField);
        
        initializeDiseaseAutocomplete(newField.querySelector('.disease-input'));

        diseaseFieldCount++;
    };

    window.removeDiseaseField = function (field) {
        field.remove();
    };

    function initializeDiseaseAutocomplete(inputField) {
        fetch('/diseases')
            .then(response => response.json())
            .then(data => {
                const sourceData = data.concat(["None"]);
                $j(inputField).autocomplete({
                    source: sourceData,
                    minLength: 1
                });
    
                if (!$j(inputField).val()) {
                    $j(inputField).val("None");
                }
            })
            .catch(error => console.error('Error:', error));
    }

    initializeDiseaseAutocomplete(document.querySelector('.disease-input'));

    function initializLocationAutocomplete(inputField) {
        fetch('/locations')
            .then(response => response.json())
            .then(data => {
                const sourceData = data.concat(["None"]);
                $j(inputField).autocomplete({
                    source: sourceData,
                    minLength: 1
                });
    
            })
            .catch(error => console.error('Error:', error));
    }

    initializLocationAutocomplete(document.querySelector('.location-input'));
});
