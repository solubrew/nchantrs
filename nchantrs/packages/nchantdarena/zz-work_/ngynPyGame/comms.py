









def text_objects(text, font):
	textSurface = font.render(text, True, colors['red'])
	return textSurface, textSurface.get_rect()


def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',115)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((dw/2), (dh/2))
	gameDisplay.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(2)
	gameLoop()