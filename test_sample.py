import io
from unittest import TestCase, mock
from robot_moves import report, move, left, right, place_robot


class Test_Initial(TestCase):
    def test_report(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as print_out:
            report()
            self.assertEquals(print_out.getvalue().rstrip(),
                              "Output: 0,0,NORTH")

    def test_move(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as print_out:
            move()
            move()
            report()
            self.assertEquals(print_out.getvalue().rstrip(),
                              "Output: 0,2,NORTH")

    def test_outleft(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as print_out:
            place_robot(5, 5, "SOUTH")
            move()
            left()
            move()
            move()
            right()
            report()
            self.assertEquals(print_out.getvalue().rstrip(),
                              "Output: 0,1,WEST")
