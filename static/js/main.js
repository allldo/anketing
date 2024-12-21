document.addEventListener("DOMContentLoaded", () => {
  chooseImg();

  const urlPath = window.location.pathname
  
  if (urlPath.includes('register')) {
  }

  if (urlPath.includes('dashboard') || urlPath.includes('moderator')) {
    makeAccordeon()
  }

  if (urlPath.includes('dashboard')) {
    toggleForms()
    chooseFileDocument('choose-file-doc', 'choose-file-doc-input')
    chooseFileDocument('choose-doc', 'choose-file-input')
    chooseFileDocument('choose-logo', 'choose-logo-input')
    calculateRevenue()

    addRow('positioning')
    addRow('revenue')
    addRow('employees')
    addRow('awards')
    addRow('events')

    deleteRow('positioning')
    deleteRow('revenue')
    deleteRow('employees')
    deleteRow('awards')
    deleteRow('events')
  }

  if (urlPath.includes('moderator')) {
    makeSubAccordeon('mod-archive')
    makeSubAccordeon('ankets')
    makeSubAccordeon('participans')

    chooseImgModerator()
    toggleFormsModerator()
  }
})

function chooseImg() {
  const inputImg = document.querySelector('#id_company_logo')
  const inputImgBtn =  document.querySelector('.register-img__btn')
  const inputImgBtnDelete =  document.querySelector('.register-img__btn--delete')
  const imgText = document.querySelector('.register-img__text-title')
  const img = document.querySelector('.register-img__img')
  const startImgSrc = img?.src

  if (inputImgBtn && inputImg) {
    inputImgBtn.addEventListener('click', (e) => {
      e.preventDefault()
      inputImg.click()
    })
  }

  if (inputImgBtn && inputImg && inputImgBtnDelete) {
    
      inputImg.addEventListener('change', (e) => {
        const files = e.target.files
    
        if (files.length) {

          if (!startImgSrc.length) {
            img.style.display="block"
          }

          img.src = URL.createObjectURL(files[0])

          imgText.textContent = files[0].name
          inputImgBtnDelete.classList.remove('hidden')
        } else {
          imgText.textContent = ''
          inputImgBtnDelete.classList.add('hidden')
          img.style.display="none"
        }
      })
    
      inputImgBtnDelete.addEventListener('click', () => {
        img.src = startImgSrc

        if (!startImgSrc.length) {
          img.style.display="none"
        }

        inputImg.value = ''
        imgText.textContent = ''
        inputImgBtnDelete.classList.add('hidden')
      })
  }
}

function chooseImgModerator() {
  const generalList = document.querySelector('.general-list')
  const generalItems = generalList.querySelectorAll('.general-list__item')
  for (const item of generalItems) {
    const input = item.querySelector('input')
    const btn = item.querySelector('button')
    const imgText = item.querySelector('.general-list__item-link')

    btn.addEventListener('click', () => {
      input.click()
    })

    input.addEventListener('change', (e) => {
      const files = e.target.files
    
      if (files.length) {
        imgText.textContent = files[0].name
      } else {
        imgText.textContent = ''
      }
    })
  }
}

function chooseImgLogo() {
  const btnsList = document.querySelector('.survey_form__btns')
  const chooseLogoBtn = btnsList.querySelector('#choose-logo')
  const input = btnsList.querySelector('#choose-logo-input')

  chooseLogoBtn.addEventListener('click', () => {
    input.click()
  })
}

function chooseDocument() {
  const btnsList = document.querySelector('.survey_form__btns')
  const chooseDocBtn = btnsList.querySelector('#choose-doc')
  const input = btnsList.querySelector('#choose-doc-input')

  chooseDocBtn.addEventListener('click', () => {
    input.click()
  })
}

function chooseFileDocument(btnId, inputId) {
  const btnsList = document.querySelector('.survey_form__btns')
  const chooseFileBtn = btnsList.querySelector(`#${btnId}`)
  const input = btnsList.querySelector(`#${inputId}`)

  const filesList = document.querySelector('.form-files-list')
  const filesListItems = filesList.querySelectorAll('.files-list__item')

  chooseFileBtn.addEventListener('click', () => {
    input.click()
  })

  input.addEventListener('change', (e) => {
    const files = e.target.files

    if (files.length) {
      for (const file of files) {
        const li = document.createElement('li')
        li.classList.add('files-list__item')
        const p = document.createElement('p')
        p.classList.add('files-list__item-text')
        p.innerHTML = file.name

        const btn = document.createElement('button')
        btn.classList.add('files-list__item-delete')

        const img = document.createElement('img')
        img.src = '../static/images/chrest.svg'

        btn.appendChild(img)

        li.appendChild(p)
        li.appendChild(btn)
        filesList.appendChild(li)
      }
    }
  })

  if (filesListItems && filesListItems.length) {
    for (let i = 0; i < filesListItems.length; i++) {
      const btnDelete = filesListItems[i].querySelector('button')

      btnDelete.addEventListener('click', () => {
        filesListItems[i].remove()
      })
    }
  }
}

function makeAccordeon() {
  const accordeon = document.querySelector('.accordeon')
  const accordeonItems = accordeon.querySelectorAll('.accordeon-item')
  for (const item of accordeonItems) {
    item.addEventListener('click', async (e) => {
      for (const item of accordeonItems) {
        const accordeonBody = item.querySelector('.accordeon-body')
        const accordeonPlus = item.querySelector('.accordeon-item__open-symbol--plus')
        const accordeonMinus = item.querySelector('.accordeon-item__open-symbol--minus')

        if (!accordeonBody.classList.contains('hidden')) {
          accordeonBody.classList.add('hidden')
          accordeonPlus.classList.remove('hidden')
          accordeonMinus.classList.add('hidden')
        }
      }
      

      const accordeonBody = item.querySelector('.accordeon-body')
      const accordeonPlus = item.querySelector('.accordeon-item__open-symbol--plus')
      const accordeonminus = item.querySelector('.accordeon-item__open-symbol--minus')

      accordeonBody.classList.remove('hidden')
      accordeonPlus.classList.add('hidden')
      accordeonminus.classList.remove('hidden')

      const subAccordeon = item.querySelector('.subaccordeon')

      if (subAccordeon) {
        const subItems = subAccordeon.querySelectorAll('.subaccordeon-item')

        for (const item of subItems) {
          const accordeonBody = item.querySelector('.subaccordeon-body')
          const accordeonPlus = item.querySelector('.subaccordeon-item__open-symbol--plus')
          const accordeonminus = item.querySelector('.subaccordeon-item__open-symbol--minus')

          accordeonBody.classList.add('hidden')
          accordeonPlus.classList.remove('hidden')
          accordeonminus.classList.add('hidden')
        }
      }

    })
  }
}

function makeSubAccordeon(id) {
  const accordeon = document.querySelector(`.subaccordeon#${id}`)
  const accordeonItems = accordeon.querySelectorAll('.subaccordeon-item')
  
  for (const item of accordeonItems) {
    item.addEventListener('click', (e) => {
      e.stopPropagation()
      for (const item of accordeonItems) {
        const accordeonBody = item.querySelector('.subaccordeon-body')
        const accordeonPlus = item.querySelector('.subaccordeon-item__open-symbol--plus')
        const accordeonminus = item.querySelector('.subaccordeon-item__open-symbol--minus')

        if (!accordeonBody.classList.contains('hidden')) {
          accordeonBody.classList.add('hidden')
          accordeonPlus.classList.remove('hidden')
          accordeonminus.classList.add('hidden')
        }
      }
      

      const accordeonBody = item.querySelector('.subaccordeon-body')
      const accordeonPlus = item.querySelector('.subaccordeon-item__open-symbol--plus')
      const accordeonminus = item.querySelector('.subaccordeon-item__open-symbol--minus')

      accordeonBody.classList.remove('hidden')
      accordeonPlus.classList.add('hidden')
      accordeonminus.classList.remove('hidden')
    })
  }
}

function toggleForms() {
  const profile = document.querySelector('.accordeon-body.profile')
  const changeBtn = profile.querySelector('#btn-change-form')
  const submitBtn = profile.querySelector('#btn-submit-form')
  const downloadFile = profile.querySelector('.register-img__btn.btn-primary--disabled')
  const inputs = profile.querySelectorAll('input')

  for (const input of inputs) {
    input.disabled = true
  }

  changeBtn.addEventListener('click', () => {
    for (const input of inputs) {
      input.disabled = false
    }

    downloadFile.classList.remove('btn-primary--disabled')
    downloadFile.classList.add('btn-primary')

    changeBtn.disabled = true
    changeBtn.classList.add('btn-primary--disabled')
    changeBtn.classList.remove('btn-primary')

    submitBtn.disabled = false
    submitBtn.classList.remove('btn-primary--disabled')
    submitBtn.classList.add('btn-primary')
  })
}

function toggleFormsModerator() {
  const list =  document.querySelectorAll('.subaccordeon-body.profile')
  const headers = document.querySelectorAll('.subaccordeon-header__company')

  for (const header of headers) {
    header.addEventListener('click', () => {
      for (const item of list) {
        const inputs = item.querySelectorAll('input')

        for (const input of inputs) {
          input.disabled = true
        } 
      }
    })
  }

  for (const item of list) {
    const changeBtn = item.querySelector('#btn-change-form')
    const submitBtn = item.querySelector('#btn-submit-form')
    const downloadFile = item.querySelector('.register-img__btn.btn-primary--disabled')
    const inputs = item.querySelectorAll('input')

    for (const input of inputs) {
      input.disabled = true
    }

    changeBtn.addEventListener('click', () => {
      for (const input of inputs) {
        input.disabled = false
      }

      downloadFile.classList.remove('btn-primary--disabled')
      downloadFile.classList.add('btn-primary')
  
      changeBtn.disabled = true
      changeBtn.classList.add('btn-primary--disabled')
      changeBtn.classList.remove('btn-primary')
  
      submitBtn.disabled = false
      submitBtn.classList.remove('btn-primary--disabled')
      submitBtn.classList.add('btn-primary')
    })
  }
}

function calculateRevenue() {
    let totalRevenue = 0;
    const revenue_inputs = document.querySelectorAll(".revenue-input")
    revenue_inputs.forEach((input) => {
    const value = parseFloat(input.value) || 0;
    console.log(input.value)
    totalRevenue += value;
  });
  revenue.querySelector("#total-revenue").innerText =
      new Intl.NumberFormat("ru-RU").format(totalRevenue * 1000) + " руб.";
}

function updateCategoryCounts() {
  const categoryCounts = {
      A: { awards: 0, shortlist: 0, grandprix: 0 },
      B: { awards: 0, shortlist: 0, grandprix: 0 },
      C: { awards: 0, shortlist: 0, grandprix: 0 },
  };

  // const categs
  document.querySelectorAll(".input-row").forEach((row) => {
    const categorySelect = row.querySelector(".category-select");
    const typeSelect = row.querySelector(".type-select");
        console.log(categorySelect, typeSelect)
    if (categorySelect && typeSelect) {
      const category = categorySelect.value;
      const type = typeSelect.value;

      if (categoryCounts[category]) {
        if (type === "shortlist") {
          categoryCounts[category].shortlist += 1;
        } else if (type === "award") {
          categoryCounts[category].awards += 1;
        } else if (type === "grandprix") {
          categoryCounts[category].grandprix += 1;
        }
      }
    }
  });

  document.getElementById("category-a-awards").innerText =
      categoryCounts.A.awards;
  document.getElementById("category-a-shortlist").innerText =
      categoryCounts.A.shortlist;

  document.getElementById("category-a-grandprix").innerText =
      categoryCounts.A.grandprix;

  document.getElementById("category-b-awards").innerText =
      categoryCounts.B.awards;
  document.getElementById("category-b-shortlist").innerText =
      categoryCounts.B.shortlist;

  document.getElementById("category-b-grandprix").innerText =
      categoryCounts.B.grandprix;

  document.getElementById("category-c-awards").innerText =
      categoryCounts.C.awards;
  document.getElementById("category-c-shortlist").innerText =
      categoryCounts.C.shortlist;
  document.getElementById("category-c-grandprix").innerText =
      categoryCounts.C.grandprix;

}

function addRow(id) {
  const formGroup = document.querySelector(`#${id}`)

  const btnAdd = formGroup.querySelector('.btn-str')


  btnAdd.addEventListener('click', () => {
    const formGroup = document.querySelector(`#${id}`)
    const inputRows = formGroup.querySelector('.input-rows')
    const rowList = inputRows.querySelectorAll('.input-row')

    const lastRow = rowList[rowList.length - 1]
    const newRow = lastRow.cloneNode(true);

    const inputs = newRow.querySelectorAll('input, select');
    const deleteButton = newRow.querySelector('.input-row__btn-delete');

       inputs.forEach(input => {
        if (input.name) {
            input.name = input.name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`);
        }
        if (input.id) {
            input.id = input.id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`);
        }

        if (input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        } else if (input.type === 'number') {
            input.value = 0;
        } else {
            input.value = '';
        }
    });

    inputRows.appendChild(newRow);


     const checkboxes = formGroup.querySelector('.form-group-checkboxes')
     const checkboxesItems = checkboxes.querySelectorAll('input[type="hidden"]')

     const lastCheckbox = checkboxesItems[checkboxesItems.length - 2]
     const lastCheckboxDelete = checkboxesItems[checkboxesItems.length - 1]
     const cloneLastCheckbox = lastCheckbox.cloneNode(true)
     const clonelastCheckboxDelete = lastCheckboxDelete.cloneNode(true)

     cloneLastCheckbox.name = cloneLastCheckbox.name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
     cloneLastCheckbox.id = cloneLastCheckbox.id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
     cloneLastCheckbox.removeAttribute('value')
     clonelastCheckboxDelete.name = clonelastCheckboxDelete.name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
     clonelastCheckboxDelete.id = clonelastCheckboxDelete.id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)

     checkboxes.appendChild(cloneLastCheckbox)
     checkboxes.appendChild(clonelastCheckboxDelete)

     const checkboxName = cloneLastCheckbox.name.split('-')[0]
     const inputForDjango = document.querySelector(`input[name=${checkboxName}-TOTAL_FORMS]`)
     const inputForDjangoValue = Number(inputForDjango.getAttribute('value'))
     inputForDjango.setAttribute('value', inputForDjangoValue + 1)
  })
}

function deleteRow(id) {
  const formGroup = document.querySelector(`#${id}`)
  const inputRows = formGroup.querySelector('.input-rows')
  const rowList = inputRows.querySelectorAll('.input-row')

  const inputsList = formGroup.querySelector('.form-group-checkboxes')
  const inputListItems = inputsList.querySelectorAll('input[type="hidden"]')

  for (const row of rowList) {
    const btnDelete = row.querySelector('.input-row__btn-delete')

    btnDelete.addEventListener('click', () => {
      const parent = btnDelete.parentElement

      if (inputRows.childElementCount < 2) {
        console.log('many');
        return
      }

      const index = Array.from(inputRows.children).indexOf(parent)
      inputRows.removeChild(parent)

      console.log('inputListItemsinputListItems', inputListItems);
      for (const input of inputListItems) {
        if (input.name.includes('mask_for_deletion')) {
          const inputId = Number(input.getAttribute('name').match(/-(\d+)-/)[1])
          if (inputId === index) {
            input.value = 'DELETE'
          }
        }
      }
      
    })
  }

}