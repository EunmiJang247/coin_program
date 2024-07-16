interface FailedProps {
  logic: {
    [propName: string | symbol]: any;
    errorMessage?: string | undefined;
  };
}

const Failed: React.FC<FailedProps> = ({ logic }) => {
  return <div>에러가 발생했습니다.: {(logic as any).errorMessage ?? '알 수 없는 에러'}</div>;
};

export default Failed;
