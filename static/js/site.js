let formsetContainer = document.querySelectorAll(
        '.formset-container'
    );
    form = document.querySelector('#form');
    addFormsetButton = document.querySelector('#add-formset');
    totalForms = document.querySelector('#id_form-TOTAL_FORMS');
    formsetNum = formsetContainer.length - 1;

    addFormsetButton.addEventListener('click', $addFormset);

    function $addFormset(e) {
        e.preventDefault();

        let newForm = formsetContainer[0].cloneNode(true);
            formRegex = RegExp('FORM-(\\D){1}-', 'g');
        
            formsetNum++
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, 'form-${formsetNum}-');
            form.insertBefore(newForm, addFormsetButton);

            totalForms.setAttribute('value', '${formsetNum + 1}');
    }
