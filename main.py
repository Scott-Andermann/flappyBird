import neat

from game_main import game_main
from flappy_birt_neat import eval_genomes

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

gen = 0
if __name__ == '__main__':
    config_path = 'config_feedforward.txt'
    run(config_path)

    #game_main()
