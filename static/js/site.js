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

    function $gotoSPA_Page() {
        const input = document.getElementById("seller-id");
        const container = document.getElementById("details");
        const id = input.value;
        var url = `/seller-token/${id}/`;

        fetch (url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "2be586765275c87b57d640c4250b59710a1aa387",
                "User": "Mary",
            }
        }).then(async(response) => {
            return await response.text();
        }).then(async(data) => {
            const thisData = await data;
            container.innerHTML =  await data;
        });
    }
