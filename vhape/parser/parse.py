"""
Vhape DSL Parser

Parses Gherkin-style steps to extract structured information about
API security testing scenarios.
"""

from pathlib import Path
from typing import Dict, Optional, Literal
from lark import Lark, Tree, Token
from lark.exceptions import LarkError


class DSLParseError(Exception):
    """Exception raised when DSL parsing fails."""
    pass


class StepParser:
    """
    Parser for Vhape DSL steps.
    
    Parses Gherkin-style steps and extracts structured information
    about tokens, endpoints, and validations.
    """
    
    def __init__(self):
        """Initialize the parser with the grammar file."""
        grammar_path = Path(__file__).parent / "grammar.lark"
        
        if not grammar_path.exists():
            raise FileNotFoundError(f"Grammar file not found: {grammar_path}")
        
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar = f.read()
        
        self.parser = Lark(
            grammar,
            start='start',
            parser='lalr',
            lexer='standard',
        )
    
    def parse_step(self, step_text: str) -> Dict:
        """
        Parse a single step text and return structured information.
        
        Args:
            step_text: The step text to parse (e.g., "Given I have a valid token")
            
        Returns:
            Dictionary with step type and extracted information:
            - type: 'given', 'when', or 'then'
            - token_type: 'valid', 'admin', 'user', 'invalid', or 'none' (for given)
            - endpoint: endpoint string (for when)
            - validation: 'validate_token', 'expect_401', 'access_denied', or 'access_allowed' (for then)
            
        Raises:
            DSLParseError: If the step cannot be parsed
        """
        try:
            step_text = step_text.strip()
            tree = self.parser.parse(step_text)
            return self._extract_info(tree)
        except LarkError as e:
            raise DSLParseError(f"Failed to parse step: {step_text}\nError: {e}")
    
    def _extract_info(self, tree: Tree) -> Dict:
        """Extract structured information from the parse tree."""
        # The tree structure is: start -> step -> (given_step|when_step|then_step)
        # We need to unwrap these levels
        current = tree
        
        # Unwrap 'start' if present
        if current.data == 'start':
            current = current.children[0]
        
        # Unwrap 'step' if present
        if current.data == 'step':
            current = current.children[0]
        
        # Now we should have the actual step type
        if current.data == 'given_step':
            return self._extract_given(current)
        elif current.data == 'when_step':
            return self._extract_when(current)
        elif current.data == 'then_step':
            return self._extract_then(current)
        else:
            raise DSLParseError(f"Unknown step type: {current.data}")
    
    def _extract_given(self, tree: Tree) -> Dict:
        """Extract information from a Given step."""
        # Structure: given_step -> token_context -> token_type -> (valid_token|admin_token|...)
        token_context = tree.children[0]  # token_context
        token_type_node = token_context.children[0]  # token_type
        actual_token = token_type_node.children[0]  # valid_token, admin_token, etc.
        
        token_type_name = actual_token.data
        
        token_type_map = {
            'valid_token': 'valid',
            'admin_token': 'admin',
            'user_token': 'user',
            'invalid_token': 'invalid',
            'no_token': 'none',
        }
        
        token_type = token_type_map.get(token_type_name, 'unknown')
        
        return {
            'type': 'given',
            'token_type': token_type,
        }
    
    def _extract_when(self, tree: Tree) -> Dict:
        """Extract information from a When step."""
        # Structure: when_step -> endpoint -> Token(ESCAPED_STRING, "...")
        endpoint_tree = tree.children[0]  # endpoint
        endpoint_token = endpoint_tree.children[0]  # Token with the string
        
        # Extract the string value and remove quotes
        endpoint = str(endpoint_token.value).strip('"')
        
        return {
            'type': 'when',
            'endpoint': endpoint,
        }
    
    def _extract_then(self, tree: Tree) -> Dict:
        """Extract information from a Then step."""
        # Structure: then_step -> validation -> (validate_token|expect_401|...)
        validation_tree = tree.children[0]  # validation
        actual_validation = validation_tree.children[0]  # validate_token, expect_401, etc.
        
        validation_name = actual_validation.data
        
        validation_map = {
            'validate_token': 'validate_token',
            'expect_401': 'expect_401',
            'access_denied': 'access_denied',
            'access_allowed': 'access_allowed',
        }
        
        validation = validation_map.get(validation_name, 'unknown')
        
        return {
            'type': 'then',
            'validation': validation,
        }


# Convenience function for parsing steps
def parse_step(step_text: str) -> Dict:
    """
    Parse a step text and return structured information.
    
    Args:
        step_text: The step text to parse
        
    Returns:
        Dictionary with parsed step information
        
    Example:
        >>> parse_step("Given I have a valid token")
        {'type': 'given', 'token_type': 'valid'}
        
        >>> parse_step('When I send a request to "/api/users/me"')
        {'type': 'when', 'endpoint': '/api/users/me'}
        
        >>> parse_step("Then the response should validate token")
        {'type': 'then', 'validation': 'validate_token'}
    """
    parser = StepParser()
    return parser.parse_step(step_text)


if __name__ == "__main__":
    # Test the parser
    parser = StepParser()
    
    test_steps = [
        "Given I have a valid token",
        "Given I have an admin token",
        "Given I have a user token",
        "Given I have an invalid token",
        "Given I have no token",
        'When I send a request to "/api/users/me"',
        'When I send a request to "/api/admin/users"',
        "Then the response should validate token",
        "Then the response should expect 401",
        "Then the response should access denied",
        "Then the response should access allowed",
    ]
    
    print("Testing Vhape DSL Parser\n" + "=" * 50)
    
    for step in test_steps:
        try:
            result = parser.parse_step(step)
            print(f"✓ {step}")
            print(f"  → {result}\n")
        except DSLParseError as e:
            print(f"✗ {step}")
            print(f"  → Error: {e}\n")

