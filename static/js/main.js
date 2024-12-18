document.addEventListener("DOMContentLoaded", () => {
  const urlPath = window.location.pathname
  
  if (urlPath.includes('register') || urlPath.includes('dashboard')) {
    chooseImg();
//    chooseImgSurvey()
  }

  if (urlPath.includes('dashboard')) {
    makeAccordeon()
    toggleForms()
    makeSubAccordeon()
  }

  if (urlPath.includes('moderator')) {
    makeAccordeon()
    makeSubAccordeon()
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

function chooseImgSurvey() {
  const inputImg = document.querySelector('#survey_loader')
  const inputImgBtn =  document.querySelector('.load_file_survey')
//  const inputImgBtnDelete =  document.querySelector('.register-img__btn--delete')
  const imgText = document.querySelector('.load_file_survey_text')

  console.log('inputImgBtnSurvey', inputImgBtn);

  if (inputImgBtn) {
    inputImgBtn.addEventListener('click', (e) => {
      console.log('inputImg', inputImg);
      e.preventDefault()
      inputImg.click()
    })
  }

  if (inputImgBtn) {

      inputImg.addEventListener('change', (e) => {
        const files = e.target.files

        if (files.length) {
          imgText.textContent = files[0].name
//          inputImgBtnDelete.classList.remove('hidden')
        } else {
          imgText.textContent = ''
//          inputImgBtnDelete.classList.add('hidden')
        }
        console.log('e', e);
      })

//      inputImgBtnDelete.addEventListener('click', () => {
//        console.log('inputImg', inputImg.value);
//        inputImg.value = ''
//        imgText.textContent = ''
////        inputImgBtnDelete.classList.add('hidden')
//        console.log('files', inputImg.value);
//      })
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
        const accordeonminus = item.querySelector('.accordeon-item__open-symbol--minus')

        if (!accordeonBody.classList.contains('hidden')) {
          accordeonBody.classList.add('hidden')
          accordeonPlus.classList.remove('hidden')
          accordeonminus.classList.add('hidden')
        }
      }
      

      const accordeonBody = item.querySelector('.accordeon-body')
      const accordeonPlus = item.querySelector('.accordeon-item__open-symbol--plus')
      const accordeonminus = item.querySelector('.accordeon-item__open-symbol--minus')

      accordeonBody.classList.remove('hidden')
      accordeonPlus.classList.add('hidden')
      accordeonminus.classList.remove('hidden')
    })
  }
}

function makeSubAccordeon() {
  const accordeon = document.querySelector('.subaccordeon')
  const accordeonItems = accordeon.querySelectorAll('.subaccordeon-item')

  for (const item of accordeonItems) {
    item.addEventListener('click', async (e) => {
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