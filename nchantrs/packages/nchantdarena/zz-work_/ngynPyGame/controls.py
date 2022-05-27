








class keyboard:

class mouse:

class joystick:

class screen:

		''
		ctrlmap = {
					'lvl0': {
						'chk0': {
							'if': pygame.Quit,
							'then': self.quit()
						},
					},
					'lvl1': {
						'chk0': {
							'if': pygame.KEYDOWN
							'then':
								'chk0':

					}

		for lvl in ctrlmap.keys():
			for check in lvl:
				if event.type == check:
			self.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						x_delta = -1
					elif event.key == pygame.K_RIGHT:
						x_delta = 1
				if event.type == pygame.KEYUP:
					x_delta = 0
				print(event)