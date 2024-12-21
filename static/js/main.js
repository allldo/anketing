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
    addRow('positioning')

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
          console.log('files', files);

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
  console.log('toggle');
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
  const revenue = document.querySelector(".form-group.revenue")
  const revenueInputs = revenue.querySelectorAll(".input-row__item.price");
  let totalRevenue = 0;

  revenueInputs.forEach((input) => {
      const value = parseFloat(input.value) || 0;
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
  console.log("start");
  document.querySelectorAll(".awards_section").forEach((row) => {
      const category = row.querySelector(".category-select").value;
      const type = row.querySelector(".type-select").value;
      console.log("gogo");
      console.log(category);
      console.log(type);
      if (type === "shortlist") {
      console.log(categoryCounts[category].shortlist);
          categoryCounts[category].shortlist += 1;
      } else if (type === "award") {
          categoryCounts[category].awards += 1;
      }
      else if (type === "grandprix"){
          categoryCounts[category].grandprix += 1;
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
  const inputRows = formGroup.querySelector('.input-rows')
  const rowList = inputRows.querySelectorAll('.input-row')
  const btnAdd = formGroup.querySelector('.btn-str')  

  console.log('formGroup', formGroup);
  console.log('rowList', rowList);
  console.log('btnAdd', btnAdd);
  
  btnAdd.addEventListener('click', () => {
    const lastRow = rowList[rowList.length - 1]
    console.log('lastRow', lastRow);
    const lastRowItems = lastRow.querySelectorAll('.input-row__item')
    const btnDelete = lastRow.querySelector('.input-row__btn-delete')
    const cloneBtnDelete = btnDelete.cloneNode(true)
    
    const row = document.createElement('div')
    row.classList.add('input-row')

    for (const item of lastRowItems) {
      const inputItem = document.createElement('div')
      inputItem.classList.add('input-row__item')

      const cloneChild = item.children[1].cloneNode(true)
      console.log('cloneChildcloneChild', cloneChild);
      if (typeof cloneChild?.children[1]?.selectedIndex === 'number') {
        console.log('cloneChild.children[0]', cloneChild.children[0]);
        console.log('cloneChild.children[1]', cloneChild.children[1]);
        cloneChild.children[0].value = ''
        cloneChild.children[0].name = cloneChild.children[0].name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
        cloneChild.children[0].id = cloneChild.children[0].id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
        cloneChild.children[1].selectedIndex = 0
        cloneChild.children[1].name = cloneChild.children[1].name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
        cloneChild.children[1].id = cloneChild.children[1].id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
      } else {
        if (cloneChild.getAttribute('type') === 'number') {
          cloneChild.setAttribute('value', '0')
        } else {
          cloneChild.setAttribute('value', '')
        }
        console.log('cloneChild', cloneChild);
        console.log('cloneChild.name', cloneChild.name);
        cloneChild.name = cloneChild.name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
        cloneChild.id = cloneChild.id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
      }
      console.log('cloneChild', cloneChild);
      inputItem.appendChild(cloneChild)
      
      row.append(inputItem)
    }

    row.append(cloneBtnDelete)
    console.log('row', row);
    
    inputRows.appendChild(row)

    const checkboxes = formGroup.querySelector('.form-group-checkboxes')
    const checkboxesItems = checkboxes.querySelectorAll('input[type="checkbox"]')
    const lastCheckbox = checkboxesItems[checkboxesItems.length - 1]
    const cloneLastCheckobx = lastCheckbox.cloneNode(true)

    console.log('cloneLastCheckobx', cloneLastCheckobx);
    console.log('cloneLastCheckobx.id', cloneLastCheckobx.id);
    cloneLastCheckobx.name = cloneLastCheckobx.name.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
    cloneLastCheckobx.id = cloneLastCheckobx.id.replace(/-(\d+)-/, (_, num) => `-${+num + 1}-`)
    checkboxes.appendChild(cloneLastCheckobx)
    console.log('cloneLastCheckobx', cloneLastCheckobx)

    const checkboxName = cloneLastCheckobx.name.split('-')[0]
    console.log('checkboxName', cloneLastCheckobx.name.split('-')[0]);
    const inputForDjango = document.querySelector(`input[name=${checkboxName}-TOTAL_FORMS]`)
    const inputForDjangoValue = Number(inputForDjango.getAttribute('value'))
    inputForDjango.setAttribute('value', inputForDjangoValue + 1)
    console.log('inputForDjango', inputForDjango.getAttribute('value'));
  })
}
