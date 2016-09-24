from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import VMobject

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.numerals import *
from scene import Scene
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from mobject.vectorized_mobject import *

from eola.matrix import *
from eola.two_d_space import *
from eola.chapter1 import plane_wave_homotopy
from eola.chapter3 import ColumnsToBasisVectors
from eola.chapter5 import NameDeterminant, Blob
from eola.chapter9 import get_small_bubble
from eola.chapter10 import ExampleTranformationScene

class Student(PiCreature):
    CONFIG = {
        "name" : "Student"
    }
    def get_name(self):
        text = TextMobject(self.name)
        text.add_background_rectangle()
        text.next_to(self, DOWN)
        return text

class PhysicsStudent(Student):
    CONFIG = {
        "color" : PINK,
        "name" : "Physics student"
    }

class CSStudent(Student):
    CONFIG = {
        "color" : PURPLE_E,
        "flip_at_start" : True,
        "name" : "CS Student"
    } 

class OpeningQuote(Scene):
    def construct(self):
        words = TextMobject(
            "``Such",
            "axioms,", 
            "together with other unmotivated definitions,", 
            "serve mathematicians mainly by making it",
            "difficult for the uninitiated",
            "to master their subject, thereby elevating its authority.''",
            enforce_new_line_structure = False,
            alignment = "",
        )
        words.highlight_by_tex("axioms,", BLUE)
        words.highlight_by_tex("difficult for the uninitiated", RED)
        words.scale_to_fit_width(2*SPACE_WIDTH - 2)
        words.to_edge(UP)
        author = TextMobject("-Vladmir Arnold")
        author.highlight(YELLOW)
        author.next_to(words, DOWN, buff = 2*MED_BUFF)

        self.play(Write(words, run_time = 8))
        self.dither()
        self.play(FadeIn(author))
        self.dither(3)

class RevisitOriginalQuestion(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("Let's revisit ", "\\\\ an old question")
        self.random_blink()
        question = TextMobject("What are ", "vectors", "?", arg_separator = "")
        question.highlight_by_tex("vectors", YELLOW)
        self.teacher_says(
            question,
            added_anims = [
                ApplyMethod(self.get_students()[i].change_mode, mode)
                for i, mode in enumerate([
                    "pondering", "raise_right_hand", "erm"
                ])
            ]
        )
        self.random_blink(2)

class WhatIsA2DVector(LinearTransformationScene):
    CONFIG = {
        "v_coords" : [1, 2],
        "show_basis_vectors" : False,
        "include_background_plane" : False,
        "foreground_plane_kwargs" : {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_HEIGHT,
            "secondary_line_ratio" : 1
        },
    }
    def construct(self):
        self.plane.fade()
        self.introduce_vector_and_space()
        self.bring_in_students()

    def introduce_vector_and_space(self):
        v = Vector(self.v_coords)
        coords = Matrix(self.v_coords)
        coords.add_to_back(BackgroundRectangle(coords))
        coords.next_to(v.get_end(), RIGHT)

        two_d_vector = TextMobject(
            "``Two-dimensional ", "vector", "''", 
            arg_separator = ""
        )
        two_d_vector.highlight_by_tex("vector", YELLOW)
        two_d_vector.add_background_rectangle()
        two_d_vector.to_edge(UP)

        self.play(
            Write(two_d_vector),
            ShowCreation(v),
            Write(coords),
            run_time = 2
        )
        self.dither()
        self.v, self.coords = v, coords

    def bring_in_students(self):
        everything = self.get_mobjects()
        v, coords = self.v, self.coords
        physics_student = PhysicsStudent()
        cs_student = CSStudent()
        students = [physics_student, cs_student]
        for student, vect in zip(students, [LEFT, RIGHT]):
            student.change_mode("confused")
            student.to_corner(DOWN+vect, buff = 2*MED_BUFF)
            student.look_at(v)
            student.bubble = get_small_bubble(
                student, height = 4, width = 4,
            )
        self.play(*map(FadeIn, students))
        self.play(Blink(physics_student))
        self.dither()
        for student, vect in zip(students, [RIGHT, LEFT]):
            for mob in v, coords:
                mob.target = mob.copy()
                mob.target.scale(0.7)
            arrow = TexMobject("\\Rightarrow")
            group = VGroup(v.target, arrow, coords.target)
            group.arrange_submobjects(vect)
            student.bubble.add_content(group)
            student.v, student.coords = v.copy(), coords.copy()
            student.arrow = arrow

            self.play(
                student.change_mode, "pondering",
                ShowCreation(student.bubble),
                Write(arrow),
                Transform(student.v, v.target),
                Transform(student.coords, coords.target),
            )
            self.play(Blink(student))
            self.dither()
        anims = []
        for student in students:
            v, coords = student.v, student.coords
            v.target = v.copy()
            coords.target = coords.copy()
            group = VGroup(v.target, coords.target)
            group.arrange_submobjects(DOWN)
            group.scale_to_fit_height(coords.get_height())
            group.next_to(student.arrow, RIGHT)
            student.q_marks = TexMobject("???")
            student.q_marks.gradient_highlight(BLUE, YELLOW)
            student.q_marks.next_to(student.arrow, LEFT)
            anims += [
                Write(student.q_marks),
                MoveToTarget(v),
                MoveToTarget(coords),
                student.change_mode, "erm",
                student.look_at, student.bubble
            ]
        cs_student.v.save_state()
        cs_student.coords.save_state()
        self.play(*anims)
        for student in students:
            self.play(Blink(student))
        self.dither()
        self.play(*it.chain(
            map(FadeOut, everything + [
                physics_student.bubble,
                physics_student.v,
                physics_student.coords,
                physics_student.arrow,
                physics_student.q_marks,
                cs_student.q_marks,
            ]),
            [ApplyMethod(s.change_mode, "plain") for s in students],
            map(Animation, [cs_student.bubble, cs_student.arrow]),
            [mob.restore for mob in cs_student.v, cs_student.coords],
        ))
        bubble = cs_student.get_bubble("speech", width = 4, height = 3)
        bubble.set_fill(BLACK, opacity = 1)
        bubble.next_to(cs_student, UP+LEFT)
        bubble.write("Consider higher \\\\ dimensions")
        self.play(
            cs_student.change_mode, "speaking",
            ShowCreation(bubble),
            Write(bubble.content)
        )
        self.play(Blink(physics_student))
        self.dither()

class HigherDimensionalVectorsNumerically(Scene):
    def construct(self):
        words = VGroup(*map(TextMobject, [
            "4D vector", 
            "5D vector", 
            "100D vector", 
        ]))
        words.arrange_submobjects(RIGHT, buff = LARGE_BUFF*2)
        words.to_edge(UP)
        vectors = VGroup(*map(Matrix, [
            [3, 1, 4, 1],
            [5, 9, 2, 6, 5],
            [3, 5, 8, "\\vdots", 0, 8, 6]
        ]))
        colors = [YELLOW, MAROON_B, GREEN]
        for word, vector, color in zip(words, vectors, colors):
            vector.shift(word.get_center()[0]*RIGHT)
            word.highlight(color)
            vector.highlight(color)

        for word in words:
            self.play(FadeIn(word))
        self.play(Write(vectors))
        self.dither()
        for index, dim, direction in (0, 4, RIGHT), (2, 100, LEFT):
            v = vectors[index]
            v.target = v.copy()
            brace = Brace(v, direction)
            brace.move_to(v)
            v.target.next_to(brace, -direction)
            text = brace.get_text("%d numbers"%dim)            
            self.play(
                MoveToTarget(v),
                GrowFromCenter(brace),
                Write(text)
            )
            entries = v.get_entries()
            num_entries = len(list(entries))
            self.play(*[
                Transform(
                    entries[i],
                    entries[i].copy().scale_in_place(1.2).highlight(WHITE),
                    rate_func = squish_rate_func(
                        there_and_back, 
                        i/(2.*num_entries), 
                        i/(2.*num_entries)+0.5
                    ),
                    run_time = 2                    
                )
                for i in range(num_entries)
            ])
            self.dither()

class HyperCube(VMobject):
    CONFIG = {
        "color" : BLUE_C,
        "color2" : BLUE_D, 
        "dims" : 4,
    }
    def generate_points(self):
        corners = np.array(map(np.array, it.product(*[(-1, 1)]*self.dims)))
        def project(four_d_array):
            result = four_d_array[:3]
            w = four_d_array[self.dims-1]
            scalar = interpolate(0.8, 1.2 ,(w+1)/2.)
            return scalar*result
        for a1, a2 in it.combinations(corners, 2):
            if sum(a1==a2) != self.dims-1:
                continue
            self.add(Line(project(a1), project(a2)))
        self.pose_at_angle()
        self.gradient_highlight(self.color, self.color2)

class AskAbout4DPhysicsStudent(Scene):
    def construct(self):
        physy = PhysicsStudent().to_edge(DOWN).shift(2*LEFT)
        compy = CSStudent().to_edge(DOWN).shift(2*RIGHT)
        for pi1, pi2 in (physy, compy), (compy, physy):
            pi1.look_at(pi2.eyes)
        physy.bubble = physy.get_bubble("speech", width = 5, height = 4.5)

        line = Line(LEFT, RIGHT, color = BLUE_B)
        square = Square(color = BLUE_C)
        square.scale_in_place(0.5)
        cube = HyperCube(color = BLUE_D, dims = 3)
        hyper_cube = HyperCube()
        thought_mobs = []
        for i, mob in enumerate([line, square, cube, hyper_cube]):
            mob.scale_to_fit_height(2)            
            tex = TexMobject("%dD"%(i+1))
            tex.next_to(mob, UP)
            group = VGroup(mob, tex)
            thought_mobs.append(group)
            group.shift(
                physy.bubble.get_top() -\
                tex.get_top() + MED_BUFF*DOWN
            )
        line.shift(DOWN)
        curr_mob = thought_mobs[0]

        self.add(compy, physy)
        self.play(
            compy.change_mode, "confused",
            physy.change_mode, "hooray",
            ShowCreation(physy.bubble),
            Write(curr_mob, run_time = 1),
        )
        self.play(Blink(compy))
        for i, mob in enumerate(thought_mobs[1:]):
            self.play(Transform(curr_mob, mob))
            self.remove(curr_mob)
            curr_mob = mob
            self.add(curr_mob)
            if i%2 == 1:
                self.play(Blink(physy))
            else:
                self.dither()
        self.play(Blink(compy))
        self.dither()

class ManyCoordinateSystems(LinearTransformationScene):
    CONFIG = {
        "v_coords" : [2, 1],
        "include_background_plane" : False,
        "foreground_plane_kwargs" : {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_WIDTH,
            "secondary_line_ratio" : 1
        },
    }
    def construct(self):
        self.title = TextMobject("Many possible coordinate systems")
        self.title.add_background_rectangle()
        self.title.to_edge(UP)
        self.add_foreground_mobject(self.title)
        self.v = Vector(self.v_coords)
        self.play(ShowCreation(self.v))
        self.add_foreground_mobject(self.v)

        t_matrices = [
            [[0.5, 0.5], [-0.5, 0.5]],
            [[1, -1], [-3, -1]],
            [[-1, 2], [-0.5, -1]],
        ]
        movers = [self.plane, self.i_hat, self.j_hat]
        for mover in movers:
            mover.save_state()
        for t_matrix in t_matrices:
            self.animate_coordinates()
            self.play(*it.chain(
                map(FadeOut, movers),
                map(Animation, self.foreground_mobjects)
            ))
            for mover in movers:
                mover.restore()
            self.apply_transposed_matrix(t_matrix, run_time = 0)
            self.play(*it.chain(
                map(FadeIn, movers),
                map(Animation, self.foreground_mobjects)
            ))
        self.animate_coordinates()


    def animate_coordinates(self):
        self.i_hat.save_state()
        self.j_hat.save_state()
        cob_matrix = np.array([
            self.i_hat.get_end()[:2],
            self.j_hat.get_end()[:2]
        ]).T
        inv_cob = np.linalg.inv(cob_matrix)
        coords = np.dot(inv_cob, self.v_coords)
        array = Matrix(map(DecimalNumber, coords))
        array.get_entries()[0].highlight(X_COLOR)
        array.get_entries()[1].highlight(Y_COLOR)
        array.add_to_back(BackgroundRectangle(array))
        for entry in array.get_entries():
            entry.add_to_back(BackgroundRectangle(entry))
        array.next_to(self.title, DOWN)

        self.i_hat.target = self.i_hat.copy().scale(coords[0])
        self.j_hat.target = self.j_hat.copy().scale(coords[1])
        coord1, coord2 = array.get_entries().copy()
        for coord, vect in (coord1, self.i_hat), (coord2, self.j_hat):
            coord.target = coord.copy().next_to(
                vect.target.get_end()/2, 
                rotate_vector(vect.get_end(), -np.pi/2)
            )

        self.play(Write(array, run_time = 1))
        self.dither()
        self.play(*map(MoveToTarget, [self.i_hat, coord1]))
        self.play(*map(MoveToTarget, [self.j_hat, coord2]))
        self.play(VGroup(self.j_hat, coord2).shift, self.i_hat.get_end())
        self.dither(2)
        self.play(
            self.i_hat.restore,
            self.j_hat.restore,
            *map(FadeOut, [array, coord1, coord2])
        )

class DeterminantAndEigenvectorDontCare(LinearTransformationScene):
    CONFIG = {
        "t_matrix" : [[3, 1], [1, 2]],
        "include_background_plane" : False,
        "show_basis_vectors" : False,
        "foreground_plane_kwargs" : {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_HEIGHT,
            "secondary_line_ratio" : 1
        },
    }
    def construct(self):
        words = TextMobject(
            "Determinant", 
            "and", 
            "eigenvectors", 
            "don't \\\\ care about the coordinate system"
        )
        words.highlight_by_tex("Determinant", YELLOW)
        words.highlight_by_tex("eigenvectors", MAROON_B)
        words.add_background_rectangle()
        words.to_edge(UP)
        dark_yellow = Color(rgb = interpolate(
            color_to_rgb(YELLOW),
            color_to_rgb(BLACK),
            0.5
        ))

        blob = Blob(
            stroke_color = YELLOW,
            fill_color = dark_yellow,
            fill_opacity = 1,
        )
        blob.shift(2*LEFT+UP)
        det_label = TexMobject("A")
        det_label = VGroup(
            VectorizedPoint(det_label.get_left()).highlight(WHITE),
            det_label
        )
        det_label_target = TexMobject("\\det(M)\\cdot", "A")
        det_label.move_to(blob)

        eigenvectors = VGroup(*self.get_eigenvectors())

        self.add_foreground_mobject(words)
        self.dither()
        self.play(
            FadeIn(blob),
            Write(det_label)
        )
        self.play(
            ShowCreation(
                eigenvectors,
                submobject_mode = "one_at_a_time",
                run_time = 2,
            ),
            Animation(words)
        )
        self.dither()
        
        self.add_transformable_mobject(blob)
        self.add_moving_mobject(det_label, det_label_target)
        for vector in eigenvectors:
            self.add_vector(vector, animate = False)
        self.remove(self.plane)
        non_plane_mobs = self.get_mobjects()
        self.add(self.plane, *non_plane_mobs)
        
        cob_matrices = [
            None,
            [[1, -1], [-3, -1]],
            [[-1, 2], [-0.5, -1]],
        ] 
        def special_rate_func(t):
            if t < 0.3:
                return smooth(t/0.3)
            if t > 0.7:
                return smooth((1-t)/0.3)
            return 1
        for cob_matrix in cob_matrices:
            if cob_matrix is not None:
                self.play(
                    FadeOut(self.plane),
                    *map(Animation, non_plane_mobs)
                )
                transform = self.get_matrix_transformation(cob_matrix)
                self.plane.apply_function(transform)
                self.play(
                    FadeIn(self.plane),
                    *map(Animation, non_plane_mobs)
                )
                self.dither()
            self.apply_transposed_matrix(
                self.t_matrix,
                rate_func = special_rate_func,
                run_time = 8
            )


        

    def get_eigenvectors(self):
        vals, (eig_matrix) = np.linalg.eig(self.t_matrix.T)
        v1, v2 = eig_matrix.T
        result = []
        for v in v1, v2:
            vectors = VGroup(*[
                Vector(u*x*v)
                for x in range(7, 0, -1)
                for u in -1, 1
            ])
            vectors.gradient_highlight(MAROON_A, MAROON_C)
            result += list(vectors)
        return result

class WhatIsSpace(Scene):
    def construct(self):
        physy = PhysicsStudent()
        compy = CSStudent()
        physy.to_edge(DOWN).shift(4*LEFT)
        compy.to_edge(DOWN).shift(4*RIGHT)
        physy.make_eye_contact(compy)

        physy.bubble = get_small_bubble(physy)
        vector = Vector([1, 2])
        physy.bubble.add_content(vector)
        compy.bubble = compy.get_bubble("speech", width = 6, height = 4)
        compy.bubble.set_fill(BLACK, opacity = 1)
        compy.bubble.write("What exactly do\\\\ you mean by ``space''?")

        self.add(compy, physy)
        self.play(
            physy.change_mode, "pondering",
            ShowCreation(physy.bubble),
            ShowCreation(vector)
        )
        self.play(
            compy.change_mode, "sassy",
            ShowCreation(compy.bubble),
            Write(compy.bubble.content)
        )
        self.play(Blink(physy))
        self.dither()
        self.play(Blink(compy))
        self.dither()

class OtherVectorishThings(TeacherStudentsScene):
    def construct(self):
        words = TextMobject(
            "There are other\\\\",
            "vectorish",
            "things..."
        )
        words.highlight_by_tex("vectorish", YELLOW)
        self.teacher_says(words)
        self.change_student_modes(
            "pondering", "raise_right_hand", "erm"
        )
        self.random_blink(2)
        words = TextMobject("...like", "functions")
        words.highlight_by_tex("functions", PINK)
        self.teacher_says(words)
        self.change_student_modes(*["pondering"]*3)
        self.random_blink(2)
        self.teacher_thinks("")
        self.zoom_in_on_thought_bubble(self.get_teacher().bubble)

class FunctionGraphScene(Scene):
    CONFIG = {
        "graph_colors" : [RED, YELLOW, PINK],
        "default_functions" : [
            lambda x : (x**3 - 9*x)/20.,
            lambda x : -(x**2)/8.+1
        ],
        "default_names" : ["f", "g", "h"],
        "x_min" : -4,
        "x_max" : 4,
        "line_to_line_buff" : 0.03
    }
    def setup(self):
        self.axes = Axes(
            x_min = self.x_min,
            x_max = self.x_max,
        )
        self.add(self.axes)
        self.graphs = []

    def get_function_graph(self, func = None, animate = True, 
                           add = True, **kwargs):
        index = len(self.graphs)
        if func is None:
            func = self.default_functions[
                index%len(self.default_functions)
            ]
        default_color = self.graph_colors[index%len(self.graph_colors)]
        kwargs["color"] = kwargs.get("color", default_color)
        kwargs["x_min"] = kwargs.get("x_min", self.x_min)
        kwargs["x_max"] = kwargs.get("x_max", self.x_max)
        graph = FunctionGraph(func, **kwargs)
        if animate:
            self.play(ShowCreation(graph))
        if add:
            self.add(graph)
        self.graphs.append(graph)
        return graph

    def get_index(self, function_graph):
        if function_graph not in self.graphs:
            self.graphs.append(function_graph)
        return self.graphs.index(function_graph)

    def get_output_lines(self, function_graph, num_steps = None, nudge = True):
        index = self.get_index(function_graph)
        num_steps = num_steps or function_graph.num_steps
        lines = VGroup()
        nudge_size = index*self.line_to_line_buff
        x_min, x_max = function_graph.x_min, function_graph.x_max
        for x in np.linspace(x_min, x_max, num_steps):
            if nudge:
                x += nudge_size
            y = function_graph.function(x)
            lines.add(Line(x*RIGHT, x*RIGHT+y*UP))
        lines.highlight(function_graph.get_color())
        return lines

    def add_lines(self, output_lines):
        self.play(ShowCreation(
            output_lines,
            submobject_mode = "lagged_start",
            run_time = 2
        ))


    def label_graph(self, function_graph, name = None, animate = True):
        index = self.get_index(function_graph)
        name = name or self.default_names[index%len(self.default_names)]
        label = TexMobject("%s(x)"%name)
        label.next_to(function_graph.point_from_proportion(1), RIGHT)
        label.shift_onto_screen()
        label.highlight(function_graph.get_color())
        if animate:
            self.play(Write(label))
        else:
            self.add(label)
        return label

class AddTwoFunctions(FunctionGraphScene):
    def construct(self):
        f_graph = self.get_function_graph()
        g_graph = self.get_function_graph()
        def sum_func(x):
            return f_graph.get_function()(x)+g_graph.get_function()(x)
        sum_graph = self.get_function_graph(sum_func, animate = False)
        self.remove(sum_graph)
        f_label = self.label_graph(f_graph)
        g_label = self.label_graph(g_graph)

        f_lines = self.get_output_lines(f_graph)
        g_lines = self.get_output_lines(g_graph)
        sum_lines = self.get_output_lines(sum_graph, nudge = False)

        curr_x_point = f_lines[0].get_start()
        sum_def = self.get_sum_definition(DecimalNumber(curr_x_point[0]))
        # sum_def.scale_to_fit_width(SPACE_WIDTH-1)
        sum_def.to_corner(UP+LEFT)
        arrow = Arrow(sum_def[2].get_bottom(), curr_x_point, color = WHITE)        
        prefix = sum_def[0]
        suffix = VGroup(*sum_def[1:])
        rect = BackgroundRectangle(sum_def)
        brace = Brace(prefix)
        brace.add(brace.get_text("New function").shift_onto_screen())

        self.play(
            Write(prefix, run_time = 2),
            FadeIn(brace)
        )
        self.dither()        
        for lines in f_lines, g_lines:
            self.add_lines(lines)
        self.play(*map(FadeOut, [f_graph, g_graph]))
        self.dither()
        self.play(FadeOut(brace))
        fg_group = VGroup(*list(f_label)+list(g_label))
        self.play(
            FadeIn(rect),
            Animation(prefix),
            Transform(fg_group, suffix),
        )
        self.remove(prefix, fg_group)
        self.add(sum_def)
        self.play(ShowCreation(arrow))

        self.show_line_addition(f_lines[0], g_lines[0], sum_lines[0])
        self.dither()

        curr_x_point = f_lines[1].get_start()
        new_sum_def = self.get_sum_definition(DecimalNumber(curr_x_point[0]))
        new_sum_def.to_corner(UP+LEFT)
        new_arrow = Arrow(sum_def[2].get_bottom(), curr_x_point, color = WHITE)
        self.play(
            Transform(sum_def, new_sum_def),
            Transform(arrow, new_arrow),
        )
        self.show_line_addition(f_lines[1], g_lines[1], sum_lines[1])
        self.dither()

        final_sum_def = self.get_sum_definition(TexMobject("x"))
        final_sum_def.to_corner(UP+LEFT)
        self.play(
            FadeOut(rect),
            Transform(sum_def, final_sum_def),
            FadeOut(arrow)
        )
        self.show_line_addition(*it.starmap(VGroup, [
            f_lines[2:], g_lines[2:], sum_lines[2:]
        ]))
        self.play(ShowCreation(sum_graph))

    def get_sum_definition(self, input_mob):
        result = VGroup(*it.chain(
            TexMobject("(f+g)", "("), 
            [input_mob.copy()],
            TexMobject(")", "=", "f("),
            [input_mob.copy()],
            TexMobject(")", "+", "g("),
            [input_mob.copy()],
            TexMobject(")")
        ))
        result.arrange_submobjects()
        result[0].highlight(self.graph_colors[2])
        VGroup(result[5], result[7]).highlight(self.graph_colors[0])
        VGroup(result[9], result[11]).highlight(self.graph_colors[1])
        return result


    def show_line_addition(self, f_lines, g_lines, sum_lines):
        g_lines.target = g_lines.copy()
        dots = VGroup()
        dots.target = VGroup()
        for f_line, g_line in zip(f_lines, g_lines.target):
            align_perfectly = f_line.get_end()[1]*g_line.get_end()[1] > 0
            dot = Dot(g_line.get_end(), radius = 0.07)
            g_line.shift(f_line.get_end()-g_line.get_start())
            dot.target = Dot(g_line.get_end())            
            if not align_perfectly:
                g_line.shift(self.line_to_line_buff*RIGHT)
            dots.add(dot)
            dots.target.add(dot.target)
        for group in dots, dots.target:
            group.highlight(sum_lines[0].get_color())
        self.play(ShowCreation(dots))
        if len(list(g_lines)) == 1:
            kwargs = {}
        else:
            kwargs = {
                "submobject_mode" : "lagged_start",
                "run_time" : 3
            }
        self.play(*[
            MoveToTarget(mob, **kwargs)
            for mob in g_lines, dots
        ])
        # self.play(
        #     *[mob.fade for mob in g_lines, f_lines]+[
        #     Animation(dots)
        # ])
        self.dither()

class AddVectorsCoordinateByCoordinate(Scene):
    def construct(self):
        v1 = Matrix(["x_1", "y_1", "z_1"])
        v2 = Matrix(["x_2", "y_2", "z_2"])
        v_sum =  Matrix(["x_1 + x_2", "y_1 + y_2", "z_1 + z_2"])
        for v in v1, v2, v_sum:
            v.get_entries()[0].highlight(X_COLOR)
            v.get_entries()[1].highlight(Y_COLOR)
            v.get_entries()[2].highlight(Z_COLOR)
        plus, equals = TexMobject("+=")
        VGroup(v1, plus, v2, equals, v_sum).arrange_submobjects()

        self.add(v1, plus, v2)
        self.dither()
        self.play(
            Write(equals),
            Write(v_sum.get_brackets())
        )
        self.play(
            Transform(v1.get_entries().copy(), v_sum.get_entries()),
            Transform(v2.get_entries().copy(), v_sum.get_entries()),
        )
        self.dither()

class ScaleFunction(FunctionGraphScene):
    def construct(self):
        graph = self.get_function_graph(
            lambda x : self.default_functions[0](x),
            animate = False
        )
        scaled_graph = self.get_function_graph(
            lambda x : graph.get_function()(x)*2,
            animate = False, add = False
        )
        graph_lines = self.get_output_lines(graph)
        scaled_lines = self.get_output_lines(scaled_graph, nudge = False)

        f_label = self.label_graph(graph, "f", animate = False)
        two_f_label = self.label_graph(scaled_graph, "(2f)", animate = False)
        self.remove(two_f_label)

        title = TexMobject("(2f)", "(x) = 2", "f", "(x)")
        title.highlight_by_tex("(2f)", scaled_graph.get_color())
        title.highlight_by_tex("f", graph.get_color())
        title.next_to(ORIGIN, LEFT, buff = MED_BUFF)
        title.to_edge(UP)
        self.add(title)

        self.add_lines(graph_lines)
        self.dither()
        self.play(Transform(graph_lines, scaled_lines))
        self.play(ShowCreation(scaled_graph))
        self.play(Write(two_f_label))
        self.play(FadeOut(graph_lines))
        self.dither()

class ScaleVectorByCoordinates(Scene):
    def construct(self):
        two, dot, equals = TexMobject("2 \\cdot =")
        v1 = Matrix(list("xyz"))
        v1.get_entries().gradient_highlight(X_COLOR, Y_COLOR, Z_COLOR)
        v2 = v1.copy()
        two_targets = VGroup(*[
            two.copy().next_to(entry, LEFT)
            for entry in v2.get_entries()
        ])
        v2.get_brackets()[0].next_to(two_targets, LEFT)
        v2.add(two_targets)
        VGroup(two, dot, v1, equals, v2).arrange_submobjects()

        self.add(two, dot, v1)
        self.play(
            Write(equals),
            Write(v2.get_brackets())
        )
        self.play(
            Transform(two.copy(), two_targets),
            Transform(v1.get_entries().copy(), v2.get_entries())
        )
        self.dither()

class ShowSlopes(Animation):
    CONFIG = {
        "line_color" : YELLOW,
        "dx" : 0.01,
        "rate_func" : None,
        "run_time" : 5
    }
    def __init__(self, graph, **kwargs):
        digest_config(self, kwargs, locals())
        line = Line(LEFT, RIGHT, color = self.line_color)
        line.save_state()
        Animation.__init__(self, line, **kwargs)

    def update_mobject(self, alpha):
        f = self.graph.point_from_proportion        
        low, high = map(f, np.clip([alpha-self.dx, alpha+self.dx], 0, 1))
        slope = (high[1]-low[1])/(high[0]-low[0])
        self.mobject.restore()
        self.mobject.rotate(np.arctan(slope))
        self.mobject.move_to(f(alpha))

class FromVectorsToFunctions(VectorScene):
    def construct(self):
        self.show_vector_addition_and_scaling()
        self.bring_in_functions()
        self.show_derivative()

    def show_vector_addition_and_scaling(self):
        self.plane = self.add_plane()
        self.plane.fade()
        words1 = TextMobject("Vector", "addition")
        words2 = TextMobject("Vector", "scaling")
        for words in words1, words2:
            words.add_background_rectangle()
            words.next_to(ORIGIN, RIGHT).to_edge(UP)
        self.add(words1)

        v = self.add_vector([2, -1], color = MAROON_B)
        w = self.add_vector([3, 2], color = YELLOW)
        w.save_state()
        self.play(w.shift, v.get_end())
        vw_sum = self.add_vector(w.get_end(), color = PINK)
        self.dither()
        self.play(
            Transform(words1, words2),
            FadeOut(vw_sum),
            w.restore
        )
        self.add(
            v.copy().fade(),
            w.copy().fade()
        )
        self.play(v.scale, 2)
        self.play(w.scale, -0.5)
        self.dither()

    def bring_in_functions(self):
        everything = VGroup(*self.get_mobjects())
        axes = Axes()
        axes.shift(2*SPACE_WIDTH*LEFT)

        fg_scene_config = FunctionGraphScene.CONFIG
        graph = FunctionGraph(fg_scene_config["default_functions"][0])
        graph.highlight(MAROON_B)
        func_tex = TexMobject("\\frac{1}{9}x^3 - x")
        func_tex.highlight(graph.get_color())
        func_tex.shift(5.5*RIGHT+2*UP)

        words = VGroup(*[
            TextMobject(words).add_background_rectangle()
            for words in [
                "Linear transformations",
                "Null space",
                "Dot products",
                "Eigen-everything",
            ]
        ])
        words.gradient_highlight(BLUE_B, BLUE_D)
        words.arrange_submobjects(DOWN, aligned_edge = LEFT)
        words.to_corner(UP+LEFT)
        self.play(FadeIn(
            words,
            submobject_mode = "lagged_start",
            run_time = 3
        ))
        self.dither()
        self.play(*[
            ApplyMethod(mob.shift, 2*SPACE_WIDTH*RIGHT)
            for mob in axes, everything
        ] + [Animation(words)]
        )
        self.play(ShowCreation(graph), Animation(words))
        self.play(Write(func_tex, run_time = 2))
        self.dither(2)

        top_word = words[0]
        words.remove(top_word)
        self.play(
            FadeOut(words),
            top_word.shift, top_word.get_center()[0]*LEFT
        )
        self.dither()
        self.func_tex = func_tex
        self.graph = graph

    def show_derivative(self):
        func_tex, graph = self.func_tex, self.graph
        new_graph = FunctionGraph(lambda x : (x**2)/3.-1)
        new_graph.highlight(YELLOW)

        func_tex.generate_target()
        lp, rp = parens = TexMobject("()")
        parens.scale_to_fit_height(func_tex.get_height())
        L, equals = TexMobject("L=")
        deriv = TexMobject("\\frac{d}{dx}")
        new_func = TexMobject("\\frac{1}{3}x^2 - 1")
        new_func.highlight(YELLOW)
        group = VGroup(
            L, lp, func_tex.target, rp,
            equals, new_func
        )
        group.arrange_submobjects()
        group.shift(2*UP).to_edge(LEFT, buff = 2*MED_BUFF)
        rect = BackgroundRectangle(group)
        group.add_to_back(rect)
        deriv.move_to(L, aligned_edge = RIGHT)

        self.play(
            MoveToTarget(func_tex),
            *map(Write, [L, lp, rp, equals, new_func])
        )
        self.remove(func_tex)
        self.add(func_tex.target)
        self.dither()
        faded_graph = graph.copy().fade()
        self.add(faded_graph)
        self.play(
            Transform(graph, new_graph, run_time = 2),
            Animation(group)
        )
        self.dither()
        self.play(Transform(L, deriv))
        self.play(ShowSlopes(faded_graph))
        self.dither()

class TransformationsAndOperators(TeacherStudentsScene):
    def construct(self):
        self.student_says("""
            Are these the same
            as ``linear operators''?
        """, student_index = 0)
        self.random_blink()
        teacher = self.get_teacher()
        bubble = teacher.get_bubble("speech", height = 2, width = 2)
        bubble.set_fill(BLACK, opacity = 1)
        bubble.write("Yup!")
        self.play(
            teacher.change_mode, "hooray",
            ShowCreation(bubble),
            Write(bubble.content, run_time = 1)
        )
        self.random_blink(2)

class ManyFunctions(FunctionGraphScene):
    def construct(self):
        randy = Randolph().to_corner(DOWN+LEFT)
        self.add(randy)
        for i in range(100):
            if i < 3:
                run_time = 1
                self.dither()
            elif i < 10:
                run_time = 0.4
            else:
                run_time = 0.2
            added_anims = []
            if i == 3:
                added_anims = [randy.change_mode, "confused"]
            if i == 10:
                added_anims = [randy.change_mode, "pleading"]
            self.add_random_function(
                run_time = run_time,
                added_anims = added_anims
            )

    def add_random_function(self, run_time = 1, added_anims = []):
        coefs = np.random.randint(-3, 3, np.random.randint(3, 8))
        def func(x):
            return sum([c*x**(i) for i, c, in enumerate(coefs)])
        graph = self.get_function_graph(func, animate = False)
        if graph.get_height() > 2*SPACE_HEIGHT:
            graph.stretch_to_fit_height(2*SPACE_HEIGHT)
            graph.shift(graph.point_from_proportion(0.5)[1]*DOWN)
            graph.shift(interpolate(-3, 3, random.random())*UP)
        graph.highlight(random_bright_color())
        self.play(
            ShowCreation(graph, run_time = run_time),
            *added_anims
        )

class WhatDoesLinearMean(TeacherStudentsScene):
    def construct(self):
        words = TextMobject("""
            What does it mean for
            a transformation of functions
            to be """, "linear", "?",
            arg_separator = ""
        )
        words.highlight_by_tex("linear", BLUE)
        self.student_says(words)
        self.change_student_modes("pondering")
        self.random_blink(4)

class FormalDefinitionOfLinear(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False,
        "include_background_plane" : False,
        "t_matrix" : [[1, 1], [-0.5, 1]],
        "w_coords" : [1, 1],
        "v_coords" : [1, -2],        
        "foreground_plane_kwargs" : {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_HEIGHT,
            "secondary_line_ratio" : 1
        },
    }
    def construct(self):
        self.plane.fade()
        self.write_properties()
        self.show_additive_property()
        self.show_scaling_property()
        self.add_words()

    def write_properties(self):
        title = TextMobject(
            "Formal definition of linearity"
        )
        title.add_background_rectangle()
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(SPACE_WIDTH)
        h_line.next_to(title, DOWN)

        v_tex, w_tex = ["\\vec{\\textbf{%s}}"%s for s in "vw"]
        tex_sets = [
            [
                ("\\text{Additivity: }",),
                ("L(", v_tex, "+", w_tex, ")"),
                ("=", "L(", v_tex, ")", "+", "L(", w_tex, ")"),
            ],
            [
                ("\\text{Scaling: }",),
                ("L(", "c", v_tex, ")"),
                ("=", "c", "L(", v_tex, ")"),
            ],
        ]
        properties = VGroup()
        for tex_set in tex_sets:
            words = VGroup(*it.starmap(TexMobject, tex_set))
            for word in words:
                word.highlight_by_tex(v_tex, YELLOW)
                word.highlight_by_tex(w_tex, MAROON_B)
                word.highlight_by_tex("c", GREEN)
            words.arrange_submobjects()
            words.lhs = words[1]
            words.rhs = words[2]
            words.add_to_back(BackgroundRectangle(words))
            # words.scale(0.8)
            properties.add(words)
        properties.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = MED_BUFF)
        properties.next_to(h_line, DOWN, buff = 2*MED_BUFF).to_edge(LEFT)

        self.play(Write(title), ShowCreation(h_line))
        self.dither()
        for words in properties:
            self.play(Write(words))
        self.dither()
        self.add_foreground_mobject(title, h_line, *properties)
        self.additivity, self.scaling = properties

    def show_additive_property(self):
        self.plane.save_state()

        v = self.add_vector(self.v_coords)
        v_label = self.add_transformable_label(v, "v", direction = "right")
        w = self.add_vector(self.w_coords, color = MAROON_B)
        w_label = self.add_transformable_label(w, "w", direction = "left")
        w_group = VGroup(w, w_label)
        w_group.save_state()
        self.play(w_group.shift, v.get_end())
        vw_sum = self.add_vector(w.get_end(), color = PINK)
        v_label_copy, w_label_copy = v_label.copy(), w_label.copy()
        v_label_copy.generate_target()
        w_label_copy.generate_target()
        plus = TexMobject("+")
        vw_label = VGroup(v_label_copy.target, plus, w_label_copy.target)
        vw_label.arrange_submobjects()
        vw_label.next_to(vw_sum.get_end(), RIGHT)
        self.play(
            MoveToTarget(v_label_copy),
            MoveToTarget(w_label_copy),
            Write(plus)
        )
        vw_label_copy = vw_label.copy()
        vw_label = VGroup(
            VectorizedPoint(vw_label.get_left()),
            vw_label,
            VectorizedPoint(vw_label.get_right()),
        )
        self.remove(v_label_copy, w_label_copy, plus)
        self.add(vw_label)
        self.play(
            w_group.restore,
        )
        vw_label.target = VGroup(
            TexMobject("L(").scale(0.8),
            vw_label_copy,
            TexMobject(")").scale(0.8),
        )
        vw_label.target.arrange_submobjects()
        for mob in vw_label, vw_label.target:
            mob.add_to_back(BackgroundRectangle(mob))

        transform = self.get_matrix_transformation(self.t_matrix)
        point = transform(vw_sum.get_end())
        vw_label.target.next_to(point, UP)
        self.apply_transposed_matrix(
            self.t_matrix, 
            added_anims = [MoveToTarget(vw_label)]
        )
        self.dither()
        self.play(w_group.shift, v.get_end())
        v_label_copy, w_label_copy = v_label.copy(), w_label.copy()
        v_label_copy.generate_target()
        w_label_copy.generate_target()
        equals, plus = TexMobject("=+")
        rhs = VGroup(
            equals, v_label_copy.target,
            plus, w_label_copy.target
        )
        rhs.arrange_submobjects()
        rhs.next_to(vw_label, RIGHT)
        rect = BackgroundRectangle(rhs)
        self.play(*it.chain(
            map(Write, [rect, equals, plus]),
            map(MoveToTarget, [v_label_copy, w_label_copy]),
        ))
        to_fade = [self.plane, v, v_label, w_group, vw_label, vw_sum]
        to_fade += self.get_mobjects_from_last_animation()

        self.dither()
        self.play(*it.chain(
            map(FadeOut, to_fade),
            map(Animation, self.foreground_mobjects)
        ))
        self.plane.restore()
        self.play(FadeIn(self.plane), *map(Animation, self.foreground_mobjects))
        self.transformable_mobjects = []
        self.moving_vectors = []        
        self.transformable_labels = []
        self.moving_mobjects = []
        self.add_transformable_mobject(self.plane)
        self.add(*self.foreground_mobjects)

    def show_scaling_property(self):
        v = self.add_vector([1, -1])
        v_label = self.add_transformable_label(v, "v")
        scaled_v = v.copy().scale(2)
        scaled_v_label = TexMobject("c\\vec{\\textbf{v}}")
        scaled_v_label.highlight(YELLOW)
        scaled_v_label[0].highlight(GREEN)
        scaled_v_label.next_to(scaled_v.get_end(), RIGHT)
        scaled_v_label.add_background_rectangle()
        v_copy, v_label_copy = v.copy(), v_label.copy()
        self.play(
            Transform(v_copy, scaled_v),
            Transform(v_label_copy, scaled_v_label),
        )
        self.remove(v_copy, v_label_copy)
        self.add(scaled_v_label)
        self.add_vector(scaled_v, animate = False)
        self.dither()

        transform = self.get_matrix_transformation(self.t_matrix)
        point = transform(scaled_v.get_end())
        scaled_v_label.target = TexMobject("L(", "c", "\\vec{\\textbf{v}}", ")")
        scaled_v_label.target.highlight_by_tex("c", GREEN)
        scaled_v_label.target.highlight_by_tex("\\vec{\\textbf{v}}", YELLOW)
        scaled_v_label.target.scale(0.8)
        scaled_v_label.target.next_to(point, RIGHT)
        scaled_v_label.target.add_background_rectangle()

        self.apply_transposed_matrix(
            self.t_matrix, 
            added_anims = [MoveToTarget(scaled_v_label)]
        )
        self.dither()
        scaled_v = v.copy().scale(2)
        rhs = TexMobject("=", "c", "L(", "\\vec{\\textbf{v}}", ")")
        rhs.highlight_by_tex("c", GREEN)
        rhs.highlight_by_tex("\\vec{\\textbf{v}}", YELLOW)
        rhs.add_background_rectangle()
        rhs.scale(0.8)
        rhs.next_to(scaled_v_label, RIGHT)
        v_copy = v.copy()
        self.add(v_copy)
        self.play(Transform(v, scaled_v))
        self.play(Write(rhs))
        self.dither()
        faders = [
            scaled_v_label, scaled_v, v_copy, 
            v, rhs
        ] + self.transformable_labels + self.moving_vectors
        self.play(*map(FadeOut, faders))

    def add_words(self):
        randy = Randolph().shift(LEFT).to_edge(DOWN)
        bubble = randy.get_bubble("speech", width = 6, height = 4)
        bubble.set_fill(BLACK, opacity = 0.8)
        bubble.shift(0.5*DOWN)
        VGroup(randy, bubble).to_edge(RIGHT, buff = 0)
        words = TextMobject(
            "Linear transformations\\\\",
            "preserve",
            "addition and \\\\ scalar multiplication",
        )
        words.scale(0.9)
        words.highlight_by_tex("preserve", YELLOW)
        bubble.add_content(words)

        self.play(FadeIn(randy))
        self.play(
            ShowCreation(bubble),            
            Write(words),
            randy.change_mode, "speaking",
        )
        self.play(Blink(randy))
        self.dither()

class CalcStudentsKnowThatDerivIsLinear(TeacherStudentsScene):
    def construct(self):
        words = TextMobject(
            """Calc students subconsciously
            know that""",
            "$\\dfrac{d}{dx}$",
            "is linear"
        )
        words.highlight_by_tex("$\\dfrac{d}{dx}$", BLUE)
        self.teacher_says(words)
        self.change_student_modes(
            "pondering", "confused", "erm"
        )
        self.random_blink(3)

class DerivativeIsLinear(Scene):
    def construct(self):
        self.add_title()
        self.prepare_text()
        self.show_additivity()
        self.show_scaling()

    def add_title(self):
        title = TextMobject("Derivative is linear")
        title.to_edge(UP)
        self.add(title)

    def prepare_text(self):
        v_tex, w_tex = ["\\vec{\\textbf{%s}}"%s for s in "vw"]
        additivity = TexMobject(
            "L(", v_tex, "+", w_tex, ")", "=",
            "L(", v_tex, ")+L(", w_tex, ")"
        )
        scaling = TexMobject(
            "L(", "c", v_tex, ")=", "c", "L(", v_tex, ")"
        )
        for text in additivity, scaling:
            text.highlight_by_tex(v_tex, YELLOW)
            text.highlight_by_tex(w_tex, MAROON_B)
            text.highlight_by_tex("c", GREEN)

        deriv_tex = "\\dfrac{d}{dx}"
        deriv_additivity = TexMobject(
            deriv_tex, "(", "x^3", "+", "x^2", ")", "=",
            deriv_tex, "(", "x^3", ")", "+", 
            deriv_tex, "(", "x^2", ")"
        )
        deriv_scaling = TexMobject(
            deriv_tex, "(", "4", "x^3", ")", "=",
            "4", deriv_tex, "(", "x^3", ")"
        )
        for text in deriv_additivity, deriv_scaling:
            text.highlight_by_tex("x^3", YELLOW)
            text.highlight_by_tex("x^2", MAROON_B)
            text.highlight_by_tex("4", GREEN)

        self.additivity = additivity
        self.scaling = scaling
        self.deriv_additivity = deriv_additivity
        self.deriv_scaling = deriv_scaling

    def show_additivity(self):
        general, deriv = self.additivity, self.deriv_additivity
        group = VGroup(general, deriv )
        group.arrange_submobjects(DOWN, buff = 1.5)

        inner_sum = VGroup(*deriv[2:2+3])
        outer_sum_deriv = VGroup(deriv[0], deriv[1], deriv[5])
        inner_func1 = deriv[9]
        outer_deriv1 = VGroup(deriv[7], deriv[8], deriv[10])
        plus = deriv[11]
        inner_func2 = deriv[14]
        outer_deriv2 = VGroup(deriv[12], deriv[13], deriv[15])

        self.play(FadeIn(group))
        self.dither()
        self.point_out(inner_sum)
        self.point_out(outer_sum_deriv)
        self.dither()
        self.point_out(outer_deriv1, outer_deriv2)        
        self.point_out(inner_func1, inner_func2)
        self.point_out(plus)
        self.dither()
        self.play(FadeOut(group))

    def show_scaling(self):
        general, deriv = self.scaling, self.deriv_scaling
        group = VGroup(general, deriv)
        group.arrange_submobjects(DOWN, buff = 1.5)

        inner_scaling = VGroup(*deriv[2:4])
        lhs_deriv = VGroup(deriv[0], deriv[1], deriv[4])
        rhs_deriv = VGroup(*deriv[7:])
        outer_scaling = deriv[6]

        self.play(FadeIn(group))
        self.dither()
        self.point_out(inner_scaling)
        self.point_out(lhs_deriv)
        self.dither()
        self.point_out(rhs_deriv)
        self.point_out(outer_scaling)
        self.dither()

    def point_out(self, *terms):
        anims = []
        for term in terms:
            anims += [
                term.scale_in_place, 1.2,
                term.highlight, RED,
            ]
        self.play(
            *anims,
            run_time = 1,
            rate_func = there_and_back
        )

class ProposeDerivativeAsMatrix(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            """
            Let's describe the
            derivative with 
            a matrix
            """,
            pi_creature_target_mode = "hooray"
        )
        self.random_blink()
        self.change_student_modes("pondering", "confused", "erm")
        self.random_blink(3)

class PolynomialsHaveArbitrarilyLargeDegree(Scene):
    def construct(self):
        polys = VGroup(*map(TexMobject, [
            "x^{300} + 9x^2",
            "4x^{4{,}000{,}000{,}000} + 1",
            "3x^{\\left(10^{100}\\right)}",
            "\\vdots"
        ]))
        polys.gradient_highlight(BLUE_B, BLUE_D)
        polys.arrange_submobjects(DOWN, buff = 2*MED_BUFF)
        polys.scale(1.3)

        arrow = TexMobject("\\Rightarrow").scale(1.5)

        brace = Brace(
            Line(UP, DOWN).scale(SPACE_HEIGHT).shift(SPACE_WIDTH*RIGHT),
            LEFT
        )
        words = TextMobject("Infinitely many")
        words.scale(1.5)
        words.next_to(brace, LEFT)
        arrow.next_to(words, LEFT)
        polys.next_to(arrow, LEFT)

        self.play(Write(polys))
        self.dither()
        self.play(
            FadeIn(arrow),
            Write(words),
            GrowFromCenter(brace)
        )
        self.dither()

class GeneneralPolynomialCoordinates(Scene):
    def construct(self):
        poly = TexMobject(
            "a_n", "x^n", "+",
            "a_{n-1}", "x^{n-1}", "+",
            "\\cdots",
            "a_1", "x", "+",             
            "a_0", 
        )
        poly.highlight_by_tex("a_n", YELLOW)
        poly.highlight_by_tex("a_{n-1}", MAROON_B)
        poly.highlight_by_tex("a_1", RED)
        poly.highlight_by_tex("a_0", GREEN)
        poly.scale(1.3)

        array = Matrix(
            ["a_0", "a_1", "\\vdots", "a_{n-1}", "a_n", "0", "\\vdots"]
        )
        array.get_entries()[0].highlight(GREEN)
        array.get_entries()[1].highlight(RED)
        array.get_entries()[3].highlight(MAROON_B)
        array.get_entries()[4].highlight(YELLOW)
        array.scale(1.2)

        equals = TexMobject("=").scale(1.3)
        group = VGroup(poly, equals, array)
        group.arrange_submobjects()
        group.to_edge(RIGHT)

        pre_entries = VGroup(
            poly[-1], poly[-4], poly[-5], 
            poly[3], poly[0], 
            VectorizedPoint(poly.get_left()),
            VectorizedPoint(poly.get_left()),
        )

        self.add(poly, equals, array.get_brackets())
        self.dither()
        self.play(
            Transform(pre_entries.copy(), array.get_entries())
        )
        self.dither()

class SimplePolynomialCoordinates(Scene):
    def construct(self):
        matrix = Matrix(["5", "3", "1", "0", "\\vdots"])
        matrix.to_edge(LEFT)
        self.play(Write(matrix))
        self.dither()

class IntroducePolynomialSpace(Scene):
    def construct(self):
        self.add_title()
        self.show_polynomial_cloud()
        self.split_individual_polynomial()
        self.list_basis_functions()
        self.show_example_coordinates()
        self.derivative_as_matrix()

    def add_title(self):
        title = TextMobject("Our current space: ", "All polynomials")
        title.to_edge(UP)
        title[1].highlight(BLUE)
        self.play(Write(title))
        self.dither()
        self.title = title

    def show_polynomial_cloud(self):
        cloud = ThoughtBubble()[-1]
        cloud.stretch_to_fit_height(6)
        cloud.center()
        

        polys = VGroup(
            TexMobject("x^2", "+", "3", "x", "+", "5"),
            TexMobject("4x^7-5x^2"),
            TexMobject("x^{100}+2x^{99}+3x^{98}"),
            TexMobject("3x-7"),
            TexMobject("x^{1{,}000{,}000{,}000}+1"),
            TexMobject("\\vdots"),
        )
        polys.gradient_highlight(BLUE_B, BLUE_D)
        polys.arrange_submobjects(DOWN, buff = MED_BUFF)
        polys.next_to(cloud.get_top(), DOWN, buff = 2*MED_BUFF)

        self.play(ShowCreation(cloud))
        for poly in polys:
            self.play(Write(poly), run_time = 1)
        self.dither()
        self.poly1, self.poly2 = polys[0], polys[1]
        polys.remove(self.poly1)
        self.play(
            FadeOut(cloud),
            FadeOut(polys),
            self.poly1.next_to, ORIGIN, LEFT,
            self.poly1.highlight, WHITE
        )

    def split_individual_polynomial(self):
        leading_coef = TexMobject("1")
        leading_coef.next_to(self.poly1[0], LEFT, aligned_edge = DOWN)
        self.poly1.add_to_back(leading_coef)
        one = TexMobject("\\cdot", "1")
        one.next_to(self.poly1[-1], RIGHT, aligned_edge = DOWN)
        self.poly1.add(one)
        for mob in leading_coef, one:
            mob.highlight(BLACK)

        brace = Brace(self.poly1)
        brace.text = brace.get_text("Already written as \\\\ a linear combination")

        index_to_color = {
            0 : WHITE,
            1 : Z_COLOR,
            4 : Y_COLOR,
            7 : X_COLOR,
        }
        self.play(
            GrowFromCenter(brace),
            Write(brace.text),
            *[
                ApplyMethod(self.poly1[index].highlight, color)
                for index, color in index_to_color.items()
            ]
        )
        self.dither()
        self.brace = brace

    def list_basis_functions(self):
        title = TextMobject("Basis functions")
        title.next_to(self.title, DOWN, buff = MED_BUFF)
        title.to_edge(RIGHT)
        h_line = Line(ORIGIN, RIGHT).scale(title.get_width())
        h_line.next_to(title, DOWN)

        x_cubed = TexMobject("x^3")
        x_cubed.highlight(MAROON_B)
        x_cubed.to_corner(DOWN+RIGHT).shift(2*(DOWN+RIGHT))
        basis_group = VGroup(
            self.poly1[7][1],
            self.poly1[4],
            self.poly1[1],
            x_cubed
        ).copy()
        basis_group.generate_target()
        basis_group.target.arrange_submobjects(
            DOWN, buff = 0.75*LARGE_BUFF, aligned_edge = LEFT
        )
        basis_group.target.to_edge(RIGHT, buff = 2*MED_BUFF)
        dots = TexMobject("\\vdots")
        dots.next_to(basis_group.target, DOWN, buff = MED_BUFF, aligned_edge = LEFT)

        basis_functions = [
            TexMobject("b_%d(x)"%i, "=")
            for i in range(len(list(basis_group)))
        ]
        for basis_func, term in zip(basis_functions, basis_group.target):
            basis_func.highlight(term.get_color())
            basis_func.next_to(term, LEFT)
        for i in 2, 3:
            basis_functions[i].shift(SMALL_BUFF*DOWN)

        self.play(
            FadeIn(title),
            ShowCreation(h_line),
            MoveToTarget(basis_group),
            Write(dots)
        )
        for basis_func in basis_functions:
            self.play(Write(basis_func, run_time = 1))
        self.play(Write(dots))
        self.dither()
        self.basis = basis_group
        self.basis_functions = basis_functions

    def show_example_coordinates(self):
        coords = Matrix(["5", "3", "1", "0", "0", "\\vdots"])
        self.poly1.generate_target()
        equals = TexMobject("=").next_to(coords, LEFT)
        self.poly1.target.next_to(equals, LEFT)
        entries = coords.get_entries()
        entries.save_state()
        entries.set_fill(opacity = 0)

        self.play(
            MoveToTarget(self.poly1),
            Write(equals),
            FadeOut(self.brace),
            FadeOut(self.brace.text)
        )
        for entry, index in zip(entries, [6, 3, 0]):
            entry.move_to(self.poly1[index])
        self.play(Write(coords.get_brackets()))
        self.play(
            entries.restore,
            submobject_mode = "lagged_start",
            run_time = 3
        )
        self.dither()
        target = self.poly1.copy()
        terms = [
            VGroup(*target[6:8]),
            VGroup(target[5], *target[3:5]),
            VGroup(target[2], *target[0:2]),
        ]
        target[5].next_to(target[3], LEFT)
        target[2].next_to(target[0], LEFT)
        more_terms = [
            TexMobject("+0", "x^3").highlight_by_tex("x^3", MAROON_B),
            TexMobject("+0", "x^4").highlight_by_tex("x^4", YELLOW),
            TexMobject("\\vdots")
        ]        
        for entry, term in zip(entries, terms+more_terms):
            term.next_to(entry, LEFT, buff = LARGE_BUFF)
        more_terms[-1].shift(MED_BUFF*LEFT)

        self.play(Transform(self.poly1, target))
        self.dither()
        self.play(FadeIn(
            VGroup(*more_terms), 
            submobject_mode = "lagged_start",
            run_time = 2
        ))
        self.dither()

        self.play(*map(FadeOut, [self.poly1]+more_terms))
        self.poly2.next_to(equals, LEFT)
        self.poly2.shift(MED_BUFF*UP)
        self.poly2.highlight(WHITE)
        self.poly2[0].highlight(TEAL)
        VGroup(*self.poly2[3:5]).highlight(Z_COLOR)
        new_coords = Matrix(["0", "0", "-5", "0", "0", "0", "0", "4", "\\vdots"])
        new_coords.get_entries()[2].highlight(Z_COLOR)
        new_coords.get_entries()[7].highlight(TEAL)
        new_coords.scale_to_fit_height(6)
        new_coords.move_to(coords, aligned_edge = LEFT)
        self.play(
            Write(self.poly2),
            Transform(coords, new_coords)
        )
        self.dither()
        for i, mob in (2, VGroup(*self.poly2[3:5])), (7, self.poly2[0]):
            self.play(
                new_coords.get_entries()[i].scale_in_place, 1.3,
                mob.scale_in_place, 1.3,
                rate_func = there_and_back
            )
            self.remove(*self.get_mobjects_from_last_animation())
            self.dither()
        self.play(*map(FadeOut, [self.poly2, coords, equals]))

    def derivative_as_matrix(self):
        matrix = Matrix([
            ["?"]*4 + ["\\cdots"]
            for x in range(4)
        ] + [
            ["\\vdots"]*4 + ["\\ddots"]
        ])
        matrix.shift(2*LEFT)
        matrix.get_entries().gradient_highlight(GREEN, YELLOW, MAROON_B)
        mob_matrix = matrix.get_mob_matrix()
        ##Horrible
        last_col = VGroup(*mob_matrix[:,-1])
        last_col_top = last_col.get_top()
        last_col.arrange_submobjects(DOWN, buff = 0.83)
        last_col.move_to(last_col_top, aligned_edge = UP+RIGHT)
        ##End horrible
        colors = [X_COLOR, Y_COLOR, Z_COLOR, MAROON_B, YELLOW]
        for i, j in it.product(*[range(4)]*2):
            entry = mob_matrix[i, j]
            if j == i+1:
                entry.target = TexMobject(str(j))
            else:
                entry.target = TexMobject("0")
            entry.target.scale(0.8).move_to(entry)
            entry.target.highlight(colors[j])

        deriv = TexMobject("\\dfrac{d}{dx}")
        equals = TexMobject("=")
        equals.next_to(matrix, LEFT)
        deriv.next_to(equals, LEFT)

        self.play(FadeIn(deriv), FadeIn(equals))
        self.play(Write(matrix))
        self.dither()

        basis_derivatives = [
            "0",
            "1",
            "2x",
            "3x^2",
        ]
        arrays = [
            ["0", "0", "0", "0", "\\vdots"],
            ["1", "0", "0", "0", "\\vdots"],
            ["0", "2", "0", "0", "\\vdots"],
            ["0", "0", "3", "0", "\\vdots"],
        ]
        qunits = zip(
            it.count(),
            self.basis,
            self.basis_functions,
            basis_derivatives,
            arrays
        )
        for j, basis, basis_func, basis_deriv_tex, arr in qunits:
            matrix.save_state()
            matrix.generate_target()
            matrix.target.scale(0.35)
            matrix.target.to_corner(UP+LEFT)

            func, func_equals = basis_func
            deriv_copy = deriv.copy()
            movers = [func, equals, deriv_copy, basis, func_equals]
            for mob in movers:
                mob.generate_target()
                mob.save_state()
            lp, rp = TexMobject("()")
            basis_deriv = TexMobject(basis_deriv_tex)
            new_equals = TexMobject("=")
            coords = Matrix(arr)
            coords.highlight(basis.get_color())
            basis_deriv.highlight(basis.get_color())
            group = VGroup(
                func.target, equals.target, deriv_copy.target, 
                lp, basis.target, rp, func_equals.target,
                basis_deriv, new_equals, coords
            )
            group.arrange_submobjects()
            group.next_to(deriv)

            self.play(*it.chain(
                map(MoveToTarget, [
                    matrix, func, equals, 
                    deriv_copy, basis, func_equals
                ]),
                map(Write, [lp, rp])
            ))
            self.dither()
            self.play(*map(Write, [basis_deriv, new_equals, coords]))
            self.dither()
            self.play(*it.chain(
                [mob.restore for mob in movers+[matrix]],
                map(FadeOut, [lp, rp, basis_deriv, new_equals]),
                [coords.to_edge, RIGHT, 4]
            ))

            column = VGroup(*[
                mob_matrix[i,j]
                for i in range(4)
            ])
            column_target = VGroup(*[
                mob.target
                for mob in column
            ])
            entries = VGroup(*coords.get_entries()[:4])
            self.play(
                Transform(entries, column_target),
                FadeOut(coords.get_brackets()),
                FadeOut(coords.get_entries()[-1]),
                Transform(column, column_target)
            )
            self.remove(coords)
            self.dither()

class MatrixVectorMultiplicationAndDerivative(TeacherStudentsScene):
    def construct(self):
        mv_mult = VGroup(
            Matrix([[3, 1], [0, 2]]).highlight_columns(X_COLOR, Y_COLOR),
            Matrix(["x", "y"]).highlight_columns(YELLOW)
        )
        mv_mult.arrange_submobjects()
        mv_mult.scale(0.75)
        arrow = TexMobject("\\Leftrightarrow")
        deriv = TexMobject("\\dfrac{df}{dx}")
        group = VGroup(mv_mult, arrow, deriv)
        group.arrange_submobjects(buff = MED_BUFF)
        arrow.highlight(BLACK)

        teacher = self.get_teacher()
        bubble = teacher.get_bubble("speech", height = 4)
        bubble.add_content(group)

        self.play(
            teacher.change_mode, "speaking",
            ShowCreation(bubble),
            Write(group)
        )
        self.random_blink()
        group.generate_target()        
        group.target.scale(0.8)
        words = TextMobject("Linear transformations")
        h_line = Line(ORIGIN, RIGHT).scale(words.get_width())
        h_line.next_to(words, DOWN)
        group.target.next_to(h_line, DOWN, buff = MED_BUFF)
        group.target[1].highlight(WHITE)
        new_group = VGroup(words, h_line, group.target)
        bubble.add_content(new_group)

        self.play(
            MoveToTarget(group),
            ShowCreation(h_line),
            Write(words),
            self.get_teacher().change_mode, "hooray"
        )
        self.change_student_modes(*["pondering"]*3)
        self.random_blink(3)

class CompareTermsInLinearAlgebraToFunction(Scene):
    def construct(self):
        l_title = TextMobject("Linear algebra \\\\ concepts")
        r_title = TextMobject("Alternate names when \\\\ applied to functions")
        for title, vect in (l_title, LEFT), (r_title, RIGHT):
            title.to_edge(UP)
            title.shift(vect*SPACE_WIDTH/2)
        h_line = Line(LEFT, RIGHT).scale(SPACE_WIDTH)
        h_line.shift(
            VGroup(l_title, r_title).get_bottom()[1]*UP + SMALL_BUFF*DOWN
        )
        v_line = Line(UP, DOWN).scale(SPACE_HEIGHT)
        VGroup(h_line, v_line).highlight(BLUE)

        self.add(l_title, r_title)
        self.play(*map(ShowCreation, [h_line, v_line]))
        self.dither()

        lin_alg_concepts = VGroup(*map(TextMobject, [
            "Linear transformations",
            "Dot products",
            "Eigenvectors",
        ]))
        function_concepts = VGroup(*map(TextMobject, [
            "Linear operators",
            "Inner products",
            "Eigenfunctions",
        ]))
        for concepts, vect in (lin_alg_concepts, LEFT), (function_concepts, RIGHT):
            concepts.arrange_submobjects(DOWN, buff = 2*MED_BUFF, aligned_edge = LEFT)
            concepts.next_to(h_line, DOWN, buff = LARGE_BUFF)
            concepts.shift(vect*SPACE_WIDTH/2)
            concepts.gradient_highlight(YELLOW_B, YELLOW_C)

            for concept in concepts:
                self.play(Write(concept, run_time = 1))
            self.dither()

class BackToTheQuestion(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            """
            Wait...so how does
            this relate to what vectors 
            really are?
            """,
            pi_creature_target_mode = "confused"
        )
        self.random_blink(2)
        self.teacher_says(
            """
            There are many different
            vector-ish things
            """
        )
        self.random_blink(2)

class YouAsAMathematician(Scene):
    def construct(self):
        mathy = Mathematician()
        mathy.to_corner(DOWN+LEFT)
        words = TextMobject("You as a mathematician")
        words.shift(2*UP)
        arrow = Arrow(words.get_bottom(), mathy.get_corner(UP+RIGHT))
        bubble = mathy.get_bubble()

        equations = self.get_content()
        bubble.add_content(equations)

        self.add(mathy)
        self.play(Write(words, run_time = 2))
        self.play(
            ShowCreation(arrow),
            mathy.change_mode, "wave_1",
            mathy.look, OUT
        )
        self.play(Blink(mathy))
        self.dither()
        self.play(
            FadeOut(words),
            FadeOut(arrow),
            mathy.change_mode, "pondering",
            ShowCreation(bubble),
        )
        self.play(Write(equations))
        self.play(Blink(mathy))
        self.dither()

        bubble.write("Does this make any sense \\\\ for functions too?")
        self.play(
            equations.next_to, mathy.eyes, RIGHT, 2*LARGE_BUFF,
            mathy.change_mode, "confused",
            mathy.look, RIGHT,
            Write(bubble.content)
        )
        self.dither()
        self.play(Blink(mathy))

    def get_content(self):
        v_tex = "\\vec{\\textbf{v}}"
        eigen_equation = TexMobject("A", v_tex, "=", "\\lambda", v_tex)
        v_ne_zero = TexMobject(v_tex, "\\ne \\vec{\\textbf{0}}")
        det_equation = TexMobject("\\det(A-", "\\lambda", "I)=0")
        arrow = TexMobject("\\Rightarrow")

        for tex in eigen_equation, v_ne_zero, det_equation:
            tex.highlight_by_tex(v_tex, YELLOW)
            tex.highlight_by_tex("\\lambda", MAROON_B)

        lhs = VGroup(eigen_equation, v_ne_zero)
        lhs.arrange_submobjects(DOWN)
        group = VGroup(lhs, arrow, det_equation)
        group.arrange_submobjects(buff = MED_BUFF)
        return group

class ShowVectorSpaces(Scene):
    def construct(self):
        title = TextMobject("Vector spaces")
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(SPACE_WIDTH)
        h_line.next_to(title, DOWN)

        v_lines = [
            Line(
                h_line.get_center(), SPACE_HEIGHT*DOWN
            ).shift(vect*SPACE_WIDTH/3.)
            for vect in LEFT, RIGHT
        ]
        vectors = self.get_vectors()
        vectors.shift(LEFT*SPACE_WIDTH*(2./3))
        arrays = self.get_arrays()
        functions = self.get_functions()
        functions.shift(RIGHT*SPACE_WIDTH*(2./3))

        self.add(h_line, *v_lines)
        self.play(ShowCreation(
            vectors,
            submobject_mode = "one_at_a_time",
            run_time = 3
        ))
        self.play(Write(arrays))
        self.play(Write(functions))
        self.dither()
        self.play(Write(title))

    def get_vectors(self, n_vectors = 10):
        vectors = VGroup(*[
            Vector(RIGHT).scale(scalar).rotate(angle)
            for scalar, angle in zip(
                2*np.random.random(n_vectors)+0.5,
                np.linspace(0, 6, n_vectors)
            )
        ])
        vectors.gradient_highlight(YELLOW, MAROON_B)
        return vectors

    def get_arrays(self):
        arrays = VGroup(*[
            VGroup(*[
                Matrix(np.random.randint(-9, 9, 2))
                for x in range(4)
            ])
            for x in range(3)
        ])
        for subgroup in arrays:
            subgroup.arrange_submobjects(DOWN, buff = MED_BUFF)
        arrays.arrange_submobjects(RIGHT)
        arrays.scale(0.7)
        arrays.gradient_highlight(YELLOW, MAROON_B)
        return arrays

    def get_functions(self):
        functions = VGroup(*[
            TexMobject(poly)
            for poly in [
                "x^2+3x+5",
                "4x^7-5x^2",
                "x^{100}+2x^{99}+3x^{98}",
                "3x-7",
                "x^{1{,}000{,}000{,}000}+1",
                "\\vdots",
            ]
        ])
        functions.arrange_submobjects(DOWN, buff = MED_BUFF)
        functions.gradient_highlight(YELLOW, MAROON_B)
        return functions

class ToolsOfLinearAlgebra(Scene):
    def construct(self):
        words = VGroup(*map(TextMobject, [
            "Linear transformations",
            "Null space",
            "Eigenvectors",
            "Dot products",
            "$\\vdots$"
        ]))
        words.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = MED_BUFF)
        words[-1].next_to(words[-2], DOWN)
        self.play(FadeIn(
            words,
            submobject_mode = "lagged_start",
            run_time = 3
        ))
        self.dither()

class MathematicianSpeakingToAll(Scene):
    def construct(self):
        mathy = Mathematician().to_corner(DOWN+LEFT)
        others = VGroup(*[
            Randolph().flip().highlight(color)
            for color in BLUE_D, GREEN_E, GOLD_E, BLUE_C
        ])
        others.arrange_submobjects()
        others.scale(0.8)
        others.to_corner(DOWN+RIGHT)

        bubble = mathy.get_bubble("speech")
        bubble.write("""
            I don't want to think
            about all y'all's crazy
            vector spaces
        """)

        self.add(mathy, others)
        self.play(
            ShowCreation(bubble),
            Write(bubble.content),
            mathy.change_mode, "sassy",
            mathy.look_at, others
        )
        self.play(Blink(others[3]))
        self.dither()
        thought_bubble = mathy.get_bubble("thought")
        self.play(
            FadeOut(bubble.content),
            Transform(bubble, thought_bubble),
            mathy.change_mode, "speaking",
            mathy.look_at, bubble,
            *[ApplyMethod(pi.look_at, bubble) for pi in others]
        )

        vect = -bubble.get_bubble_center()
        def func(point):
            centered = point+vect
            return 10*centered/np.linalg.norm(centered)
        self.play(*[
            ApplyPointwiseFunction(func, mob)
            for mob in self.get_mobjects()
        ])

class ListAxioms(Scene):
    def construct(self):
        title = TextMobject("Rules for vectors addition and scaling")
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(SPACE_WIDTH)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)

        u_tex, v_tex, w_tex = ["\\vec{\\textbf{%s}}"%s for s in "uvw"]
        axioms = VGroup(*it.starmap(TexMobject, [
            (
                "1. \\,", 
                u_tex, "+", "(", v_tex, "+", w_tex, ")=(", 
                u_tex, "+", v_tex, ")+", w_tex
            ),
            (   "2. \\,", 
                v_tex, "+", w_tex, "=", w_tex, "+", v_tex
            ),
            (
                "3. \\,", 
                "\\text{There is a vector }", "\\textbf{0}",
                "\\text{ such that }", "\\textbf{0}+", v_tex,
                "=", v_tex, "\\text{ for all }", v_tex
            ),
            (
                "4. \\,", 
                "\\text{For every vector }", v_tex, 
                "\\text{ there is a vector }", "-", v_tex,
                "\\text{ so that }", v_tex, "+", "(-", v_tex, ")=\\textbf{0}"
            ),
            (   "5. \\,", 
                "a", "(", "b", v_tex, ")=(", "a", "b", ")", v_tex
            ),
            (  
                "6. \\,", 
                "1", v_tex, "=", v_tex
            ),
            (
                "7. \\,", 
                "a", "(", v_tex, "+", w_tex, ")", "=", 
                "a", v_tex, "+", "a", w_tex
            ),
            (
                "8. \\,", 
                "(", "a", "+", "b", ")", v_tex, "=",
                "a", v_tex, "+", "b", v_tex
            ),
        ]))
        tex_color_pairs = [
            (v_tex, YELLOW),
            (w_tex, MAROON_B),
            (u_tex, PINK),
            ("a", BLUE),
            ("b", GREEN)

        ]
        for axiom in axioms:
            for tex, color in tex_color_pairs:
                axiom.highlight_by_tex(tex, color)
        axioms.arrange_submobjects(
            DOWN, buff = 2*MED_BUFF,
            aligned_edge = LEFT
        )
        axioms.scale_to_fit_width(2*SPACE_WIDTH-1)
        axioms.next_to(h_line, DOWN, buff = MED_BUFF)

        self.play(FadeIn(
            axioms,
            submobject_mode = "lagged_start",
            run_time = 5
        ))
        self.dither()
        axioms_word = TextMobject("``Axioms''")
        axioms_word.highlight(YELLOW)
        axioms_word.scale(2)
        axioms_word.shift(SPACE_WIDTH*RIGHT/2, SPACE_HEIGHT*DOWN/2)
        self.play(Write(axioms_word, run_time = 3))
        self.dither()

class AxiomsAreInterface(Scene):
    def construct(self):
        mathy = Mathematician().to_edge(LEFT)
        mathy.change_mode("pondering")
        others = [
            Randolph().flip().highlight(color)
            for color in BLUE_D, GREEN_E, GOLD_E, BLUE_C
        ]
        others = VGroup(
            VGroup(*others[:2]),
            VGroup(*others[2:]),
        )
        for group in others:
            group.arrange_submobjects(RIGHT)
        others.arrange_submobjects(DOWN)
        others.scale(0.8)
        others.to_edge(RIGHT)
        VGroup(mathy, others).to_edge(DOWN)
        double_arrow = DoubleArrow(mathy, others)

        axioms, are, rules_of_nature = words = TextMobject(
            "Axioms", "are", "rules of nature"
        )
        words.to_edge(UP)
        axioms.highlight(YELLOW)
        an_interface = TextMobject("an interface")
        an_interface.next_to(rules_of_nature, DOWN)
        red_line = Line(
            rules_of_nature.get_left(),
            rules_of_nature.get_right(),
            color = RED
        )

        self.play(Write(words))
        self.dither()
        self.play(ShowCreation(red_line))
        self.play(Transform(
            rules_of_nature.copy(),
            an_interface
        ))
        self.dither()
        self.play(FadeIn(mathy))
        self.play(
            ShowCreation(double_arrow),
            FadeIn(others, submobject_mode = "lagged_start", run_time = 2)
        )
        self.play(axioms.copy().next_to, double_arrow, UP)
        self.play(Blink(mathy))
        self.dither()

class VectorSpaceOfPiCreatures(Scene):
    def construct(self):
        creatures = self.add_creatures()
        self.show_sum(creatures)

    def add_creatures(self):
        creatures = VGroup(*[
            VGroup(*[
                PiCreature()
                for x in range(4)
            ]).arrange_submobjects(RIGHT, buff = 1.5)
            for y in range(4)
        ]).arrange_submobjects(DOWN, buff = 1.5)
        creatures = VGroup(*it.chain(*creatures))
        creatures.scale_to_fit_height(2*SPACE_HEIGHT-1)
        for pi in creatures:
            pi.change_mode(random.choice([
                "pondering", "pondering",
                "happy", "happy", "happy",
                "confused", 
                "angry", "erm", "sassy", "hooray", 
                "speaking", "tired", 
                "plain", "plain"
            ]))
            if random.random() < 0.5:
                pi.flip()
            pi.shift(0.5*(random.random()-0.5)*RIGHT)
            pi.shift(0.5*(random.random()-0.5)*UP)
            pi.highlight(random.choice([
                BLUE_B, BLUE_C, BLUE_D, BLUE_E,
                MAROON_B, MAROON_C, MAROON_D, MAROON_E,
                GREY_BROWN, GREY_BROWN, GREY,
                YELLOW_C, YELLOW_D, YELLOW_E
            ]))
            pi.scale_in_place(random.random()+0.5)

        self.play(FadeIn(
            creatures,
            submobject_mode = "lagged_start",
            run_time = 3
        ))
        self.dither()
        return creatures

    def show_sum(self, creatures):
        def is_valid(pi1, pi2, pi3):
            if len(set([pi.get_color() for pi in pi1, pi2, pi3])) < 3:
                return False
            if pi1.is_flipped()^pi2.is_flipped():
                return False
            return True
        pi1, pi2, pi3 = pis = [random.choice(creatures) for x in range(3)]
        while not is_valid(pi1, pi2, pi3):
            pi1, pi2, pi3 = pis = [random.choice(creatures) for x in range(3)]
        creatures.remove(*pis)

        transform = Transform(pi1.copy(), pi2.copy())
        transform.update(0.5)
        sum_pi = transform.mobject
        sum_pi.scale_to_fit_height(pi1.get_height()+pi2.get_height())
        for pi in pis:
            pi.generate_target()
        plus, equals = TexMobject("+=")
        sum_equation = VGroup(
            pi1.target, plus, pi2.target,
            equals, sum_pi
        )
        sum_equation.arrange_submobjects().center()

        scaled_pi3 = pi3.copy().scale(2)
        equals2 = TexMobject("=")
        two = TexMobject("2 \\cdot")
        scale_equation = VGroup(
            two, pi3.target, equals2, scaled_pi3
        )
        scale_equation.arrange_submobjects()

        VGroup(sum_equation, scale_equation).arrange_submobjects(
            DOWN, buff = MED_BUFF
        )

        self.play(FadeOut(creatures))
        self.play(*it.chain(
            map(MoveToTarget, [pi1, pi2, pi3]),
            map(Write, [plus, equals, two, equals2]),
        ))
        self.play(
            Transform(pi1.copy(), sum_pi),
            Transform(pi2.copy(), sum_pi),
            Transform(pi3.copy(), scaled_pi3)
        )
        self.remove(*self.get_mobjects_from_last_animation())
        self.add(sum_pi, scaled_pi3)
        for pi in pi1, sum_pi, scaled_pi3, pi3:
            self.play(Blink(pi))

class MathematicianDoesntHaveToThinkAboutThat(Scene):
    def construct(self):
        mathy = Mathematician().to_corner(DOWN+LEFT)
        bubble = mathy.get_bubble("thought", height = 4)
        words = TextMobject("I don't have to worry", "\\\\ about that madness!")
        bubble.add_content(words)
        new_words = TextMobject("So long as I", "\\\\ work abstractly")
        bubble.add_content(new_words)

        self.play(
            mathy.change_mode, "hooray",
            ShowCreation(bubble),
            Write(words)
        )
        self.play(Blink(mathy))
        self.dither()
        self.play(
            mathy.change_mode, "pondering",
            Transform(words, new_words)
        )
        self.play(Blink(mathy))
        self.dither()

class TextbooksAreAbstract(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            """
            All the textbooks I found
            are pretty abstract.
            """,
            pi_creature_target_mode = "pleading"
        )
        self.random_blink(3)
        self.teacher_says(
            """
            For each new concept, 
            contemplate it for 2d space
            with grid lines...
            """
        )
        self.change_student_modes("pondering")
        self.random_blink(2)
        self.teacher_says(
            "...then in some different\\\\",
            "context, like a function space"
        )
        self.change_student_modes(*["pondering"]*2)
        self.random_blink()
        self.teacher_says(
            "Only then should you\\\\",
            "think from the axioms",
            pi_creature_target_mode = "surprised"
        )
        self.change_student_modes(*["pondering"]*3)
        self.random_blink()

class LastAskWhatAreVectors(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "So...what are vectors?",
            pi_creature_target_mode = "erm"
        )
        self.random_blink()
        self.teacher_says(
            """
            The form they take
            doesn't really matter
            """
        )
        self.random_blink()

class WhatIsThree(Scene):
    def construct(self):
        what_is, three, q_mark = words = TextMobject(
            "What is ", "3", "?",
            arg_separator = ""
        )
        words.scale(1.5)
        self.play(Write(words))
        self.dither()
        self.play(
            FadeOut(what_is),
            FadeOut(q_mark),
            three.center
        )

        triplets = [
            VGroup(*[
                PiCreature(color = color).scale(0.4)
                for color in BLUE_E, BLUE_C, BLUE_D
            ]),
            VGroup(*[HyperCube().scale(0.3) for x in range(3)]),
            VGroup(*[Vector(RIGHT) for x in range(3)]),
            TexMobject("""
                \\Big\\{
                    \\emptyset, 
                    \\{\\emptyset\\}, 
                    \\{\\{\\emptyset\\}, \\emptyset\\}
                \\Big\\}
            """)
        ]
        directions = [UP+LEFT, UP+RIGHT, DOWN+LEFT, DOWN+RIGHT]
        for group, vect in zip(triplets, directions):
            if isinstance(group, TexMobject):
                pass
            elif isinstance(group[0], Vector):
                group.arrange_submobjects(RIGHT)
                group.gradient_highlight(YELLOW, MAROON_B)
            else:
                m1, m2, m3 = group
                m2.next_to(m1, buff = MED_BUFF)
                m3.next_to(VGroup(m1, m2), DOWN, buff = MED_BUFF)
            group.next_to(three, vect, buff = LARGE_BUFF)
            self.play(FadeIn(group))
        self.dither()
        self.play(*[
            Transform(
                trip, three, 
                submobject_mode = "lagged_start",
                run_time = 2
            )
            for trip in triplets
        ])

class IStillRecommendConcrete(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("""
            I still recommend 
            thinking concretely
        """)
        self.random_blink(2)
        self.student_thinks("")
        self.zoom_in_on_thought_bubble()

class AbstractionIsThePrice(Scene):
    def construct(self):
        words = TextMobject(
            "Abstractness", "is the price\\\\"
            "of", "generality"
        )
        words.highlight_by_tex("Abstractness", YELLOW)
        words.highlight_by_tex("generality", BLUE)
        self.play(Write(words))
        self.dither()

class ThatsAWrap(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("That's all for now!")
        self.random_blink(2)

class GoodLuck(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Good luck with \\\\ your future learning!",
            pi_creature_target_mode = "hooray"
        )
        self.change_student_modes(*["happy"]*3)
        self.random_blink(3)



























