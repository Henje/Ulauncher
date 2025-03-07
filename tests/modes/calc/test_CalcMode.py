from decimal import Decimal
import pytest
from ulauncher.modes.calc.CalcMode import CalcMode, eval_expr


class TestCalcMode:

    @pytest.fixture
    def mode(self):
        return CalcMode()

    def test_is_enabled(self, mode):
        assert mode.is_enabled('5')
        assert mode.is_enabled('+2')
        assert mode.is_enabled('-5')
        assert mode.is_enabled('5+')
        assert mode.is_enabled('(5/0')
        assert mode.is_enabled('0.5/0')
        assert mode.is_enabled('0.5e3+ (11**3+-2^3)')
        assert mode.is_enabled('5%2')
        assert mode.is_enabled('sqrt(2)')
        assert mode.is_enabled('1+sin(pi/2)')

        assert not mode.is_enabled('a+b')
        assert not mode.is_enabled('sqr()+1')

    def test_eval_expr_no_floating_point_errors(self):
        assert eval_expr('110 / 3') == Decimal('36.666666666666667')
        assert eval_expr('1.1 + 2.2') == Decimal('3.3')
        assert eval_expr('sin(pi)') == Decimal('0')
        assert abs(eval_expr('e**2') - eval_expr('exp(2)')) < Decimal('1e-10')

    def test_eval_expr_syntax_variation(self):
        assert eval_expr('5.5 * 10') == Decimal('55')
        assert eval_expr('12 / 1,5') == eval_expr('12 / 1.5') == Decimal('8')
        assert eval_expr('3 ** 2') == eval_expr('3^2') == Decimal('9')
        assert eval_expr('sqrt(2)**2') == Decimal('2')
        assert eval_expr('gamma(6)') == Decimal('120')

    def test_handle_query(self, mode):
        assert mode.handle_query('3+2')[0].result == 5
        assert mode.handle_query('3+2*')[0].result == 5
        assert mode.handle_query('2-2')[0].result == 0
        assert mode.handle_query('5%2')[0].result == 1

    def test_handle_query__invalid_expr(self, mode):
        [invalid_result] = mode.handle_query('3++')
        assert invalid_result.name == 'Error!'
        assert invalid_result.description == 'Invalid expression'
