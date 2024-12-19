document.addEventListener("DOMContentLoaded", () => {
  const urlPath = window.location.pathname
  
  if (urlPath.includes('register') || urlPath.includes('dashboard')) {
    chooseImg();
    toggleForms()
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
    toggleFormsModerator()
  }
})

function chooseImg() {
  const inputImg = document.querySelector('#id_company_logo')
  const inputImgBtn =  document.querySelector('.register-img__btn')
  const inputImgBtnDelete =  document.querySelector('.register-img__btn--delete')
  const imgText = document.querySelector('.register-img__text-title')

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
          imgText.textContent = files[0].name
          inputImgBtnDelete.classList.remove('hidden')
        } else {
          imgText.textContent = ''
          inputImgBtnDelete.classList.add('hidden')
        }
      })
    
      inputImgBtnDelete.addEventListener('click', () => {
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

function chooseFileDocument() {
  const btnsList = document.querySelector('.survey_form__btns')
  const chooseFileBtn = btnsList.querySelector('#choose-file-doc')
  const input = btnsList.querySelector('#choose-doc-input')

  const filesList = document.querySelector('.form-files-list')
  const filesListItems = filesList.querySelectorAll('.files-list__item')
  const btnDeleteList = filesList.querySelectorAll('button')

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

  submitBtn.addEventListener('click', () => {
    for (const input of inputs) {
      input.disabled = true
    }
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

    submitBtn.addEventListener('click', () => {
      for (const input of inputs) {
        input.disabled = true
      }
    })
  }
}