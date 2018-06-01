describe ('myFirstTest', function(){
	it("visits my app", function(){
		cy.visit('http://localhost:8080/')
		cy.contains("Hello")
		cy.get('input.autofill').should('have.attr', 'placeholder', 'Name')
		.type('Mike')
	})
})