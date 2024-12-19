document.addEventListener("DOMContentLoaded", () => {
  const urlPath = window.location.pathname
  
  if (urlPath.includes('register') || urlPath.includes('dashboard')) {
    chooseImg();
  }

  if (urlPath.includes('dashboard')) {
    makeAccordeon()
    toggleForms()
    makeSubAccordeon('current-archive')
    chooseImgLogo()
    chooseDocument()
    chooseFileDocument()
  }

  if (urlPath.includes('moderator')) {
    chooseImg()
    makeAccordeon()
    makeSubAccordeon('mod-archive')
    makeSubAccordeon('ankets')
    makeSubAccordeon('participans')

    chooseImgModerator()
    chooseDocument()

    validateCheckboxes()
  }
})

function chooseImg() {
  const inputImg = document.querySelector('#id_company_logo')
  const inputImgBtn =  document.querySelector('.register-img__btn')
  const inputImgBtnDelete =  document.querySelector('.register-img__btn--delete')
  const imgText = document.querySelector('.register-img__text-title')

  console.log('inputImgBtnzxc', inputImgBtn);

  if (inputImgBtn && inputImg) {
    inputImgBtn.addEventListener('click', (e) => {
      console.log('inputImg', inputImg);
      e.preventDefault()
      inputImg.click()
    })
  }

  if (inputImgBtn && inputImg && inputImgBtnDelete) {
    
      inputImg.addEventListener('change', (e) => {
        const files = e.target.files
    
        if (files.length) {
          imgText.textContent = files[0].name
          inputImgBtnDelete.classList.remove('hidden')
        } else {
          imgText.textContent = ''
          inputImgBtnDelete.classList.add('hidden')
        }
        console.log('e', e);
      })
    
      inputImgBtnDelete.addEventListener('click', () => {
        console.log('inputImg', inputImg.value);
        inputImg.value = ''
        imgText.textContent = ''
        inputImgBtnDelete.classList.add('hidden')
        console.log('files', inputImg.value);
      })
  }
}

function chooseImgModerator() {
  const generalList = document.querySelector('.general-list')
  const generalItems = generalList.querySelectorAll('.general-list__item')
  console.log('generalItems', generalItems);
  for (const item of generalItems) {
    const input = item.querySelector('input')
    const btn = item.querySelector('button')
    const imgText = item.querySelector('.general-list__item-link')
    console.log('imgText', imgText);

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
      console.log('e', e);
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

function chooseFileDocument() {
  const btnsList = document.querySelector('.survey_form__btns')
  const chooseFileBtn = btnsList.querySelector('#choose-file-doc')
  const input = btnsList.querySelector('#choose-doc-input')

  const filesList = document.querySelector('.form-files-list')
  const filesListItems = filesList.querySelectorAll('.files-list__item')
  const btnDeleteList = filesList.querySelectorAll('button')
  console.log('filesList', filesList);

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
      console.group('Accordeon')
      console.log('accordeon', accordeon);
      console.groupEnd()
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
  console.log('id', id);
  console.log('subaccordeonItems', accordeonItems);
  
  for (const item of accordeonItems) {
    item.addEventListener('click', (e) => {
      e.stopPropagation()
      console.group('Subaccordeon')
      console.log('id', id);
      console.log('accordeon', accordeon);
      console.groupEnd()
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
  const changeBtn = document.querySelector('#btn-change-form')
  const submitBtn = document.querySelector('#btn-submit-form')
  const profile = document.querySelector('.accordeon-body.profile')
  const inputs = profile.querySelectorAll('input')

  console.log('inputs', inputs);

  for (const input of inputs) {
    input.disabled = true
  }

  changeBtn.addEventListener('click', () => {
    for (const input of inputs) {
      input.disabled = false
    }

    changeBtn.disabled = true
    changeBtn.classList.add('btn-primary--disabled')
    changeBtn.classList.remove('btn-primary')

    submitBtn.disabled = false
    submitBtn.classList.remove('btn-primary--disabled')
    submitBtn.classList.add('btn-primary')
  })
}

function validateCheckboxes() {

}