import SubCategory from '../../data-types/sub-category';

const useReadSubCategories = () => {
  return async (): Promise<SubCategory[]> => {
    // TODO 원래는 서버로부터 가져와야 함.

    return [
      {
        id: '1',
        name: '육개장',
        slug: 'yukgaejang',
      },
      {
        id: '2',
        name: '치킨',
        slug: 'chicken',
      },
      {
        id: '3',
        name: '한솥',
        slug: 'hansot',
      },
      {
        id: '4',
        name: '에그드랍',
        slug: 'eggdrop',
      },
      {
        id: '5',
        name: '으아니 차',
        slug: 'uanicha',
      },
    ];
  };
};

export default useReadSubCategories;
