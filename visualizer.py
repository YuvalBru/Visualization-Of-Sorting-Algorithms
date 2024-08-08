import pygame
import random
import math

pygame.init()
pygame.mixer.init()
complete_sound = pygame.mixer.Sound("complete_sound.mp3")
pygame.mixer.music.load("kahoot_sound.mp3")
background_sound_not_sorting = "kahoot_sound.mp3"
pygame.mixer.music.load("super_mario_song.mp3")
background_sound_sorting = "super_mario_song.mp3"
background = pygame.image.load("background.png")
icon = pygame.image.load("icon.png")


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Yuval's Sorting Mini-Game")
        pygame.display.set_icon(icon)
        self.window.blit(background, (0,0))
        self.set_list(lst)


    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):

    draw_info.window.blit(background,(0,0))

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                        draw_info.RED)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1,
                                     draw_info.WHITE)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting1 = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort", 1,
                                     draw_info.WHITE)
    sorting2 = draw_info.FONT.render("| Q - Quick Sort| H - Heap sort |C - Cocktail Shaker Sort", 1, draw_info.WHITE)

    l_inst = draw_info.FONT.render("To leave the game press 'L'", 1, draw_info.WHITE)

    draw_info.window.blit(sorting1, (draw_info.width / 2 - sorting1.get_width() / 2, 75))
    draw_info.window.blit(sorting2, (draw_info.width / 2 - sorting2.get_width() / 2, 105))
    draw_info.window.blit(l_inst, (draw_info.width / 2  - l_inst.get_width() - 300, 3 ))
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BLACK, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    complete_sound.play()
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    complete_sound.play()
    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        if ascending:
            min_index = i
            for j in range(i+1, len(lst)):
                if lst[j] < lst[min_index]:
                    min_index = j
        else:
            min_index = len(lst) - 1 - i
            for j in range(len(lst) -1-i):
                if lst[j] < lst[min_index]:
                    min_index = j

        if min_index != i and ascending:
            lst[i], lst[min_index] = lst[min_index], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
            yield True

        if min_index != len(lst) - 1 - i and not ascending:
            lst[len(lst) - 1 - i], lst[min_index] = lst[min_index], lst[len(lst) - 1 - i]
            draw_list(draw_info, {len(lst) - 1 - i: draw_info.GREEN, min_index: draw_info.RED}, True)
            yield True

    complete_sound.play()
    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    if len(lst) == 0:
        return []
    return merge_sort_(0, len(lst) - 1, lst, ascending, draw_info, n)

def merge_sort_(lo, hi, lst, ascending, draw_info, n):
    if lo == hi:
        return [lst[lo]]
    mid = (lo + hi) // 2
    left = yield from merge_sort_(lo, mid, lst, ascending, draw_info, n )
    right = yield from merge_sort_(mid + 1, hi, lst, ascending, draw_info, n)
    return (yield from merge(left, right, ascending, draw_info , n))

def merge(left, right, ascending, draw_info , n):
    sorted_list = []
    l, r = 0, 0

    while l < len(left) and r < len(right):
        if (left[l] < right[r] and ascending) or (left[l] > right[r] and not ascending):
            sorted_list.append(left[l])
            l += 1
        else:
            sorted_list.append(right[r])
            r += 1

        draw_info.lst = sorted_list + left[l:] + right[r:]
        draw_list(draw_info, {l - 1: draw_info.GREEN, r: draw_info.RED}, True)
        yield True

    while l < len(left):
        sorted_list.append(left[l])
        l += 1
        draw_info.lst = sorted_list + left[l:] + right[r:]
        draw_list(draw_info, {l - 1: draw_info.GREEN}, True)
        yield True

    while r < len(right):
        sorted_list.append(right[r])
        r += 1
        draw_info.lst = sorted_list + left[l:] + right[r:]
        draw_list(draw_info, {r - 1: draw_info.RED}, True)
        yield True
    if len(sorted_list) == n:
        complete_sound.play()

    return sorted_list


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(start, end):
        pivot_index = start
        pivot = lst[pivot_index]

        while start < end:
            while start < len(lst) and ((lst[start] <= pivot and ascending) or (lst[start] >= pivot and not ascending)):
                start += 1

            while (lst[end] > pivot and ascending) or (lst[end] < pivot and not ascending):
                end -= 1

            if start < end:
                lst[start], lst[end] = lst[end], lst[start]
                draw_list(draw_info, {start: draw_info.GREEN, end: draw_info.RED}, True)
                yield True

        lst[end], lst[pivot_index] = lst[pivot_index], lst[end]
        draw_list(draw_info, {end: draw_info.GREEN, pivot_index: draw_info.RED}, True)
        yield True

        return end

    def quick_sort_recursive(start, end):
        if start < end:
            partition_index = yield from partition(start, end)
            yield from quick_sort_recursive(start, partition_index - 1)
            yield from quick_sort_recursive(partition_index + 1, end)

    yield from quick_sort_recursive(0, len(lst) - 1)
    complete_sound.play()



def heap_sort(draw_info, ascending=True):
    n = len(draw_info.lst)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(draw_info, n, i, ascending)

    for i in range(n - 1, 0, -1):
        draw_info.lst[i], draw_info.lst[0] = draw_info.lst[0], draw_info.lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(draw_info, i, 0, ascending)

    complete_sound.play()


def heapify(draw_info, n, i, ascending):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if ascending:
        if l < n and draw_info.lst[l] > draw_info.lst[largest]:
            largest = l
        if r < n and draw_info.lst[r] > draw_info.lst[largest]:
            largest = r
    else:
        if l < n and draw_info.lst[l] < draw_info.lst[largest]:
            largest = l
        if r < n and draw_info.lst[r] < draw_info.lst[largest]:
            largest = r

    if largest != i:
        draw_info.lst[i], draw_info.lst[largest] = draw_info.lst[largest], draw_info.lst[i]
        draw_list(draw_info, {i: draw_info.RED, largest: draw_info.GREEN}, True)
        yield True
        yield from heapify(draw_info, n, largest, ascending)


def cocktail_shaker_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    start = 0
    end = n - 1
    swapped = True

    while swapped:
        swapped = False

        for i in range(start, end):
            if (lst[i] > lst[i + 1] and ascending) or (lst[i] < lst[i + 1] and not ascending):
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                swapped = True
                draw_list(draw_info, {i: draw_info.RED, i+1: draw_info.GREEN}, True)
                yield True

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end, start, -1):
            if (lst[i] < lst[i - 1] and ascending) or (lst[i] > lst[i - 1] and not ascending):
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
                swapped = True
                draw_list(draw_info, {i: draw_info.RED, i+1: draw_info.GREEN}, True)
                yield True

        start += 1

    complete_sound.play()
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    pygame.mixer.music.load(background_sound_not_sorting)
    pygame.mixer.music.play(-1)

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1400, 700, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == 0:
                pygame.mixer.music.load(background_sound_sorting)
                pygame.mixer.music.play(-1)
        else:
            if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == 0:
                pygame.mixer.music.load(background_sound_not_sorting)
                pygame.mixer.music.play(-1)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(background_sound_not_sorting)
                pygame.mixer.music.play(-1)
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(background_sound_not_sorting)
                pygame.mixer.music.play(-1)
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(background_sound_sorting)
                pygame.mixer.music.play(-1)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"
            elif event.key == pygame.K_c and not sorting:
                sorting_algorithm = cocktail_shaker_sort
                sorting_algo_name = "Cocktail Shaker Sort"
            elif event.key == pygame.K_l:
                pygame.mixer.music.stop()
                pygame.quit()

    pygame.mixer.music.stop()
    pygame.quit()



if __name__ == "__main__":
    main()
