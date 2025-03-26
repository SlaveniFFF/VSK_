document.addEventListener('DOMContentLoaded', function () {
	const animatedElement = document.querySelector('.kv')
	const numberElements = document.querySelectorAll('.text1-square')
	let animationStarted = false

	function animateNumbers() {
		if (animationStarted) return
		let animationsCompleted = 0
		numberElements.forEach(numberElement => {
			const target = parseInt(numberElement.textContent, 10)
			const duration = 2500
			const start = 0
			let current = start
			const increment = target / (duration / 8)

			function updateNumber() {
				if (current >= target) {
					current = target
				}
				numberElement.firstChild.textContent = Math.round(current)

				if (current < target) {
					current += increment
					requestAnimationFrame(updateNumber)
				} else {
					animationsCompleted++
					if (animationsCompleted === numberElements.length) {
						numberElements.forEach(element => {
							element.querySelector('span').classList.add('visible')
						})
					}
				}
			}
			updateNumber()
		})
		animationStarted = true
	}

	function checkVisibility() {
		const elementTop = animatedElement.getBoundingClientRect().top
		const windowHeight = window.innerHeight

		if (elementTop < windowHeight * 0.75) {
			animatedElement.classList.add('visible')
			animateNumbers()
		}
	}
	checkVisibility()
	window.addEventListener('scroll', checkVisibility)
})

function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}




