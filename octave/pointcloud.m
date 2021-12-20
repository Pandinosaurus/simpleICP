classdef pointcloud < handle

  properties

    x
    y
    z

    nx
    ny
    nz
    planarity

    noPoints
    sel

  endproperties

  methods

    function obj = pointcloud(x, y, z)

      obj.x = x;
      obj.y = y;
      obj.z = z;

      obj.noPoints = numel(x);

      obj.sel = transpose(1:obj.noPoints);

    endfunction

    function selectInRange(obj, X, range)

      [~, distance] = knnsearch(X, [obj.x(obj.sel) obj.y(obj.sel) obj.z(obj.sel)], 1);
      keep = distance <= range;
      obj.sel = obj.sel(keep);

    endfunction

    function selectNPoints(obj, n)

        noSelectedPoints = numel(obj.sel);

        if noSelectedPoints > n
            idx = transpose(round(linspace(1, noSelectedPoints, n)));
            obj.sel = obj.sel(idx);
        end

    endfunction

    function estimateNormals(obj, neighbors)

      obj.nx = NaN(obj.noPoints,1);
      obj.ny = NaN(obj.noPoints,1);
      obj.nz = NaN(obj.noPoints,1);
      obj.planarity = NaN(obj.noPoints,1);

      idxNN = knnsearch(...
          [obj.x obj.y obj.z], ...
          [obj.x(obj.sel) obj.y(obj.sel) obj.z(obj.sel)], ...
          neighbors);

      for i = 1:numel(obj.sel)
          C = cov([obj.x(idxNN(i,:)) obj.y(idxNN(i,:)) obj.z(idxNN(i,:))]);
          [P, latent] = pcacov(C);
          obj.nx(obj.sel(i)) = P(1,3);
          obj.ny(obj.sel(i)) = P(2,3);
          obj.nz(obj.sel(i)) = P(3,3);
          obj.planarity(obj.sel(i)) = (latent(2)-latent(3))/latent(1);
      end

    endfunction

    function transform(obj, H)

      XInH = obj.eulerCoordToHomogeneousCoord([obj.x obj.y obj.z]);
      XOutH = transpose(H*XInH');
      XOut = obj.homogeneousCoordToEulerCoord(XOutH);

      obj.x = XOut(:,1);
      obj.y = XOut(:,2);
      obj.z = XOut(:,3);

    endfunction

  endmethods

  methods (Static = true)

    function XH = eulerCoordToHomogeneousCoord(XE)

      noPoints = size(XE, 1);
      XH = [XE ones(noPoints,1)];

    endfunction

    function XE = homogeneousCoordToEulerCoord(XH)

      XE = XH(:,[1 2 3])./XH(:,4);

    endfunction

  endmethods

endclassdef
