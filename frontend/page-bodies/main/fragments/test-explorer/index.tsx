import { LoadedLogic } from '../../use-logic';
import FiltersFragment from '../filters';
import SearchFragment from '../search';
import TestFragment from '../test';

interface Props {
  logic: LoadedLogic;
}

const TestExplorerFragment: React.FC<Props> = ({ logic }) => {
  return (
    <div>
      <FiltersFragment logic={logic} />
      <div>
        <SearchFragment logic={logic} />
        <TestFragment logic={logic} />
      </div>
    </div>
  );
};

export default TestExplorerFragment;
