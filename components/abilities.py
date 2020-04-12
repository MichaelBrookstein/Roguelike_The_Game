import tcod as libtcod

from game_messages import Message

class Abilities:
    def __init__(self, ability_limit):
        self.ability_limit = ability_limit
        self.feats = []

    def add_feat(self, abilities):
        results = []

        for feat in abilities:
            if len(self.feats) >= self.ability_limit:
                results.append({
                    'consumed': False,
                    'message': Message('You cannot learn any new feats.', libtcod.yellow)
                })
            else:
                results.append({
                    'consumed': True,
                    'message': Message('You learned {0}!'.format(feat.name), libtcod.yellow)
                })
                self.feats.append(feat)

        return results

    def perform(self, feat, turn_performed, **kwargs):
        results = []

        if feat.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'targeting': feat})

        else:
            kwargs = {**feat.function_kwargs, **kwargs}
            ability_results = feat.feat_function(self.owner, **kwargs)

            results.extend(ability_results)

        if 'performed' in results[0] and results[0]['performed']:
            feat.turn_performed = turn_performed

        return results


