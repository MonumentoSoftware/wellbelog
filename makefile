# Extract the second and all subsequent words from MAKECMDGOALS
ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

$(eval $(ARG):;@true)

pytest:
	poetry run pytest $(ARG)

test_file:
	poetry run pytest test/$(ARG)